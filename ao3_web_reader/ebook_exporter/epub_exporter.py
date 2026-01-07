# https://en.wikipedia.org/wiki/EPUB
# https://www.w3.org/publishing/epub3

import os
from xml.etree import ElementTree
from xml.dom import minidom
from ao3_web_reader import models
from ao3_web_reader.ebook_exporter import BaseExporter


class EpubExporter(BaseExporter):
    def __init__(self, user_id: str, work: models.Work):
        super().__init__(user_id=user_id, work=work, logger_extra={})

    def __create_metadata_manifest_item(self, manifest_element: ElementTree.Element[str],
                                        id: str, href: str, media_type: str = "application/xhtml+xml"):

        item = ElementTree.SubElement(manifest_element, "item")

        item.attrib["id"] = id
        item.attrib["href"] = href
        item.attrib["media-type"] = media_type

    def __create_ncx_head_metadata_item(self, root_el: ElementTree.Element[str],
                                        name: str, content: str):

        item = ElementTree.SubElement(root_el, "meta")

        item.attrib["name"] = name
        item.attrib["content"] = content

    def __create_ncx_nav_point(self, root_el: ElementTree.Element[str], id: str,
                               play_order: str, chapter_title: str):

        nav_point_el = ElementTree.SubElement(root_el, "navPoint")
        nav_point_el.attrib["id"] = id
        nav_point_el.attrib["playOrder"] = play_order

        nav_label_el = ElementTree.SubElement(nav_point_el, "navLabel")
        ElementTree.SubElement(nav_label_el, "text").text = chapter_title

        content_el = ElementTree.SubElement(nav_point_el, "content")
        content_el.attrib["src"] = f"{play_order}.html"

    def __dump_to_file(self, path: str, elem: ElementTree.Element[str], pretify=True):
        with open(path, "w") as file:
            elem_str = ElementTree.tostring(
                elem, encoding="unicode", xml_declaration=True)
            
            if pretify:
                elem_str = minidom.parseString(elem_str).toprettyxml()

            file.write(elem_str)

    def __build_book_metadata_xml(self):
        package_el = ElementTree.Element("package")
        package_el.attrib["version"] = "2.0"
        package_el.attrib["xmlns"] = "http://www.idpf.org/2007/opf"
        package_el.attrib["unique-identifier"] = "uuid_id"

        # metadata
        metadata_el = ElementTree.SubElement(package_el, "metadata")
        metadata_el.attrib["xmlns:dc"] = "http://purl.org/dc/elements/1.1/"
        metadata_el.attrib["xmlns:opf"] = "http://www.idpf.org/2007/opf"

        title_el = ElementTree.SubElement(metadata_el, "dc:title")
        title_el.text = self.work.name

        language_el = ElementTree.SubElement(metadata_el, "dc:language")
        language_el.text = "en"

        creator_el = ElementTree.SubElement(metadata_el, "dc:creator")
        creator_el.text = "Unknown"

        identifier_el = ElementTree.SubElement(metadata_el, "dc:identifier")
        identifier_el.attrib["id"] = "uuid_id"
        identifier_el.attrib["opf:scheme"] = "uuid"

        identifier_el.text = f"ao3-web-reader-{self.work.work_id}"

        # manifest
        manifest_el = ElementTree.SubElement(package_el, "manifest")

        self.__create_metadata_manifest_item(
            manifest_element=manifest_el, id="titlepage", href="titlepage.xhtml")
        self.__create_metadata_manifest_item(
            manifest_element=manifest_el, id="page_css", href="page_css.css", media_type="text/css")
        self.__create_metadata_manifest_item(
            manifest_element=manifest_el, id="css", href="stylesheet.css", media_type="text/css")
        self.__create_metadata_manifest_item(
            manifest_element=manifest_el, id="ncx", href="toc.ncx", media_type="application/x-dtbncx+xml")

        for chapter_id in range(len(self.work.chapters)):
            id = chapter_id + 1

            self.__create_metadata_manifest_item(
                manifest_element=manifest_el, id=f"html{id}", href=f"{id}.html")

        # spine
        spine_el = ElementTree.SubElement(package_el, "spine")
        spine_el.attrib["toc"] = "ncx"

        itemref_el = ElementTree.SubElement(spine_el, "itemref")
        itemref_el.attrib["idref"] = "titlepage"

        for chapter_id in range(len(self.work.chapters)):
            id = chapter_id + 1

            itemref_el = ElementTree.SubElement(spine_el, "itemref")
            itemref_el.attrib["idref"] = f"html{id}"

        return package_el

    def __build_navigation_control_xml(self):
        ncx_el = ElementTree.Element("ncx")

        ncx_el.attrib["version"] = "2005-1"
        ncx_el.attrib["xml:lang"] = "en"
        ncx_el.attrib["xmlns"] = "http://www.daisy.org/z3986/2005/ncx/"

        head_el = ElementTree.SubElement(ncx_el, "head")

        self.__create_ncx_head_metadata_item(
            head_el, "dtb:uid", f"ao3-reader-{self.work.id}")
        self.__create_ncx_head_metadata_item(head_el, "dtb:depth", "2")
        self.__create_ncx_head_metadata_item(
            head_el, "dtb:generator", "ao3-web-reader (2.3.0)")
        self.__create_ncx_head_metadata_item(
            head_el, "dtb:totalPageCount", "0")
        self.__create_ncx_head_metadata_item(head_el, "dtb:maxPageNumber", "0")

        doc_title_el = ElementTree.SubElement(ncx_el, "docTitle")
        ElementTree.SubElement(doc_title_el, "text").text = self.work.name

        nav_map_el = ElementTree.SubElement(ncx_el, "navMap")

        for id, chapter in enumerate(self.work.chapters, start=1):
            self.__create_ncx_nav_point(nav_map_el, str(chapter.chapter_id),
                                        play_order=str(id), chapter_title=chapter.title)

        return ncx_el

    def export(self, output_dir_path: str):
        book_metadata_el = self.__build_book_metadata_xml()
        navigation_control_el = self.__build_navigation_control_xml()

        content_opf_path = os.path.join(output_dir_path, "content.opf")
        toc_ncx_path = os.path.join(output_dir_path, "toc.ncx")

        self.__dump_to_file(content_opf_path, book_metadata_el)
        self.__dump_to_file(toc_ncx_path, navigation_control_el)
