from flask import Flask, render_template, redirect, request, flash
from database import get_data, get_connection, delete_by_eloc

app = Flask(__name__)

app.secret_key = "supersecretkey"

def normalize_row(r):
    """Turn a DB row (dict) into a canonical place dict used by the front-end."""
    # Common name variants
    name = r.get('place_name')
    # Common latitude variants
    latitude = r.get('latitude') 
    # Common longitude variants
    longitude = r.get('longitude')
    # eLoc variants
    eloc = r.get('eloc')
    manufacturing_date = r.get('manufacturing_date')
    manufacturing_name = r.get('who_build')
    metro_station = r.get('nearest_metro_station')
    _id = r.get('id')

    # make everything strings (tojson will handle types safely)
    return {
        'id': _id,
        'name': str(name) if name is not None else '',
        'latitude': str(latitude) if latitude is not None else '',
        'longitude': str(longitude) if longitude is not None else '',
        'eloc': str(eloc) if eloc is not None else '',
        'manufacturing_date': str(manufacturing_date) if manufacturing_date is not None else '',
        'manufacture_name': str(manufacturing_name) if manufacturing_name is not None else '',
        'metro_station': str(metro_station) if metro_station is not None else ''
        # 'description': str(description) if description is not None else ''
    }

@app.route("/")
def home():
    raw = get_data() or []
    places = [normalize_row(r) for r in raw]
    # Optionally filter-out rows with no coordinates:
    # places = [p for p in places if p['latitude'] and p['longitude']]
    return render_template("index.html", places=places)

@app.route("/add", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        place_name = request.form.get("place_name")
        eloc = request.form.get("eloc")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        manufacture_date = request.form.get("manufacture_date")
        built_by = request.form.get("built_by")
        nearest_metro = request.form.get("nearest_metro")

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tourist (place_name, eloc, latitude, longitude, manufacturing_date, who_build, nearest_metro_station)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (place_name, eloc, latitude, longitude, manufacture_date, built_by, nearest_metro))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/")

    return render_template("insert_data.html")

@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        eloc = request.form.get("eloc")
        if eloc:
            deleted_rows = delete_by_eloc(eloc)
            if deleted_rows > 0:
                flash(f"Row with ELOC '{eloc}' deleted successfully!", "success")
            else:
                flash(f"No row found with ELOC '{eloc}'", "error")
        return redirect("/")

    return render_template("delete.html")



if __name__ == "__main__":
    app.run(debug=True)
