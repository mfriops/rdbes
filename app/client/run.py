#!/usr/local/bin/python3
# coding: utf-8

"""client_app.py – Thin proxy client for the *Flask Oracle Insert API*.

Single‑endpoint design
----------------------
* **One** route only: ``POST /<table>``
* ``<table>`` is the Oracle table you want to insert into (e.g. ``design`` or
  ``frequency_measure``).
* The JSON request body is forwarded untouched to the upstream API at the same
  relative path.
* A small allow‑list (``ALLOWED_TABLES``) guards against typos; set the
  ``ALLOWED_TABLES=*`` environment variable to disable validation.

Run locally
~~~~~~~~~~~
::

    $ pip install flask requests
    $ export ORACLE_API_URL="https://oracle-api.internal/api"   # upstream URL
    $ export ALLOWED_TABLES="design,sample"                     # optional
    $ flask --app client_app run --debug

Adjust ``ALLOWED_TABLES`` or extend ``DataAccessClient`` as your backend grows.
"""
from __future__ import annotations
import os
import uuid

from typing import Any, Dict, List, Set
import requests
from flask import Flask, abort, jsonify, request, render_template, flash, Response

# from api.rdbes import RdbesService
# from api.channel import ChannelService
from app.client.business.rdbes import RdbesBusiness
from app.client.business.channel import ChannelBusiness
from app.client.business.gear import GearBusiness
from app.client.business.vessel import VesselBusiness
from app.client.business.taxon import TaxonBusiness
from app.client.business.agf import AgfBusiness
from app.client.business.adb import AdbBusiness
from app.client.utils.misc import haskey

from app.client.utils.validate import combine_errors
from app.client.utils.rdbes import rdbes_existence

# ---------------------------------------------------------------------------
# Configuration helpers
# ---------------------------------------------------------------------------


def _parse_allowed_tables() -> Set[str] | None:
    env = os.environ.get("ALLOWED_TABLES")
    if not env or env == "*":
        return None  # validation disabled, accept any table name
    return {t.strip() for t in env.split(",") if t.strip()}

ALLOWED_TABLES: Set[str] | None = _parse_allowed_tables()


# ---------------------------------------------------------------------------
# Flask application factory
# ---------------------------------------------------------------------------

def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
        )

    rdbes_business = RdbesBusiness()
    channel_business = ChannelBusiness()
    taxon_business = TaxonBusiness()
    gear_business = GearBusiness()
    vessel_business = VesselBusiness()
    agf_business = AgfBusiness()
    adb_business = AdbBusiness()

    # Single generic insert route -----------------------------------------

    # A global store where we map a unique ID to (filename, content).
    download_store = {}

    @app.post("/<string:table>")
    def insert_table(table: str):
        if ALLOWED_TABLES is not None and table not in ALLOWED_TABLES:
            abort(404, description=f"Table '{table}' is not configured for inserts.")

        payload = request.get_json(force=True)  # ensure JSON
        # result = rdbes_client.insert(table, payload)
        result = rdbes_business.insert(table, payload)
        return jsonify(result), 201

    # Health‑check proxy ----------------------------------------------------

    @app.get("/rdbes-health")
    def RDBES_health():
        # return jsonify(rdbes_service.health())
        return rdbes_business.health()

    @app.get("/channel-health")
    def channel_health():
        # return jsonify(channel_service.health())
        return channel_business.health()

    @app.get("/taxon-health")
    def taxon_health():
        # return jsonify(rdbes_service.health())
        return taxon_business.health()

    @app.get("/gear-health")
    def gear_health():
        # return jsonify(rdbes_service.health())
        return gear_business.health()

    @app.get("/vessel-health")
    def vessel_health():
        # return jsonify(rdbes_service.health())
        return vessel_business.health()

    @app.get("/agf-health")
    def agf_health():
        # return jsonify(rdbes_service.health())
        return agf_business.health()

    @app.get("/adb-health")
    def adb_health():
        # return jsonify(rdbes_service.health())
        return adb_business.health()

    # Root helper -----------------------------------------------------------

    @app.route('/')
    def upload():
        return render_template('index.html')


    @app.route('/display', methods=('GET', 'POST'))
    def display():
        content = None
        if request.method == 'POST':

            action = request.form['input_button']
            if action in ('Load', 'Reload'):

                cruise = request.form['cruise']
                if cruise == '':
                    flash("Note: No action taken, cruise is missing!")
                    return render_template('index.html')

                cruiseDict = channel_business.get_cruise(cruise)
                if cruiseDict == None:
                    flash('Note: No action taken, cruise: ' + cruise + ' not found in channel!')
                    return render_template('content.html')

                retLanding = rdbes_business.set_landing(cruiseDict)

                if retLanding[0]['return'] > -1:
                    flash('Landing data successfully uploaded!')
                    return render_template('index.html')
                else:
                    flash('Note: No action taken, method Landing not implemented!')
                    # flash('Landing data upload, unsuccessful!')
                    return render_template('errors.html', error_page_html=combine_errors(retLanding[1]))

        flash('Note: No action taken, method Landing not implemented!')
        return render_template('index.html', error_page_html=None)


    @app.route('/effort', methods=('GET', 'POST'))
    def effort():
        content = None
        if request.method == 'POST':

            action = request.form['input_button']
            if action in ('Load', 'Reload'):

                cruise = request.form['cruise']
                if cruise == '':
                    flash("Note: No action taken, cruise is missing!")
                    return render_template('effort.html')

                cruiseDict = channel_business.get_cruise(cruise)
                if cruiseDict == None:
                    flash('Note: No action taken, cruise: ' + cruise + ' not found in channel!')
                    return render_template('content.html')

                retEffort = rdbes_business.write_effort(cruiseDict)

                if retEffort[0]['return'] > -1:
                    flash('Effort data successfully uploaded!')
                    return render_template('effort.html')
                else:
                    flash('Note: No action taken, method Effort not implemented!')
                    # flash('Effort data upload, unsuccessful!')
                    return render_template('errors.html', error_page_html=combine_errors(retEffort[1]))

        flash('Note: No action taken, method Effort not implemented!')
        return render_template('effort.html', error_page_html=None)


    @app.route('/sampling', methods=('GET', 'POST'))
    def sampling():
        content = None
        if request.method == 'POST':

            action = request.form['input_button']
            if action in ('Load', 'Reload'):

                cruise = request.form['cruise']
                if cruise == '':
                    flash("Note: No action taken, cruise is missing!")
                    return render_template('sampling.html')

                # If sample data for this cruise has been collencted, then stop
                # if crise_existence(cruise) > 0 and action == 'Load':
                #     flash(
                #         'Note: No action taken, sampling data for cruise: ' + cruise + ', already loaded, use reload to overwrite!')
                #     return render_template('sampling.html')

                # cruise_name = request.form['cruise']
                # if cruise_name == '':
                #     flash('Note: No action taken, cruise name is missing!!')
                #     return render_template('content.html')

                cruises = [p.strip() for p in cruise.split(',') if cruise.strip()]
                cruiseDict = []
                for cru in cruises:
                    cruiseInfo = channel_business.get_cruise(cru)
                    if not haskey(cruiseInfo,'Error'):
                        cruiseDict.append(cruiseInfo)

                if cruiseDict == []:
                    flash('Note: No action taken, cruise: ' + cruise + ' not found in channel!')
                    return render_template('content.html')

                # if action == 'Reload':
                #     if rdbes_presentation.del_sample(cruiseDict) == -1:
                #         flash('Rdbes data delete, unsuccessful!')
                #         return render_template('content.html')

                retSample = rdbes_business.write_sample(cruiseDict)

                if retSample['return'] > -1:
                    flash('Sample data successfully uploaded!')
                    return render_template('content.html')
                else:
                    flash('Sample data upload, unsuccessful!')
                    return render_template('errors.html', error_page_html=combine_errors(retSample[1]))

            elif request.form['input_button'] == 'Save csv':
                localid = request.form['localid']
                if localid == '':
                    flash("Note: No action taken, localid must be stated!")
                    return render_template('sampling.html')
                if not rdbes_existence():
                    flash("Note: No action taken, RDBES data for localid: " + localid + " are not loaded!")
                    return render_template('sampling.html')

                # 1. Define your large content and desired filename here.
                csv_data = rdbes_business.write_file(localid, 'csv')
                filename = localid + '.csv'

                # 2. Generate a unique ID and store the (filename, content) in our dictionary.
                file_id = str(uuid.uuid4())  # e.g., 'b7b...-...'
                download_store[file_id] = (filename, csv_data)

                # 3. Provide a link in the HTML that references this unique ID.
                #    The user just clicks the link to download the file.
                return f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>Download CSV File</title>
                </head>
                <body>
                    <h3p>Filename: {filename}</h3>
                    <a href="/download-file?file_id={file_id}">Download File</a>
                </body>
                </html>
                """

            elif request.form['input_button'] == 'Save xlm':
                localid = request.form['localid']
                if localid == '':
                    flash("Note: No action taken, localid must be stated!")
                    return render_template('sampling.html')
                if rdbes_existence() == 0:
                    flash("Note: No action taken, RDBES data for localid: " + localid + " are not loaded!")
                    return render_template('sampling.html')

                # 1. Define your large content and desired filename here.
                xml_data = rdbes_business.write_file(localid, 'xml')
                filename = localid + '.xml'

                # 2. Generate a unique ID and store the (filename, content) in our dictionary.
                file_id = str(uuid.uuid4())  # e.g., 'b7b...-...'
                download_store[file_id] = (filename, xml_data)

                # 3. Provide a link in the HTML that references this unique ID.
                #    The user just clicks the link to download the file.
                return f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>Download XML File</title>
                </head>
                <body>
                    <h3>Filename: {filename}</h3>
                    <a href="/download-file?file_id={file_id}">Download File</a>
                </body>
                </html>
                """

        return render_template('sampling.html', content=content)


    @app.route("/download-file")
    def download_file():
        # 4. Retrieve the file_id from the query string
        file_id = request.args.get("file_id")
        if not file_id:
            return "No file_id provided.", 400

        # 5. Look up the (filename, content). If it's missing, return an error.
        file_info = download_store.get(file_id)
        if not file_info:
            return "Invalid or expired file ID.", 404

        filename, content = file_info

        # 6. Return a Response with the specified filename and large content.
        return Response(
            content,
            mimetype="text/plain",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )


    @app.route('/about')
    def about():
        return render_template('about.html')

    return app

# ---------------------------------------------------------------------------
# Stand‑alone execution
# ---------------------------------------------------------------------------

if __name__ == "__main__":  # pragma: no cover
    app = create_app()
    app.config['SECRET_KEY'] = '98TY234234643453456RE7568820567567567FUN23445234678678432187TY03157234234TY234304'

    host = "0.0.0.0"
    port = int(os.environ.get("PORT", "5049"))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() in {"1", "true", "yes"}
    app.run(host=host, port=port, debug=debug)
