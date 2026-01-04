from flask import url_for, current_app


def get_styles_lib(local_path: str, remote_path: str):
    get_from_cdn = current_app.config.get("STYLES_LIBS_FROM_CDN")

    if not get_from_cdn:
        return url_for('static', filename=local_path)
    
    else:
        return remote_path
