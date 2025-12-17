from flask import Response
from ao3_web_reader.modules.extra import ZipTagOnTheFly


def send_tag_as_zip(user_id, works, tag_name):
    zip_on_the_fly = ZipTagOnTheFly(user_id=user_id, works=works)

    return Response(zip_on_the_fly.generator(), mimetype="application/zip", headers={
        "Content-Disposition": f"attachment; filename={tag_name}.zip"
    })
