# # # from flask import Flask, render_template, request, redirect, jsonify
# # # from database import get_db_connection
# # # from utils.generator import generate_tracking_id
# # # from urllib.parse import urlparse

# # # def valid_url(url):
# # # parsed = urlparse(url)
# # # # #     return parsed.scheme in ("http", "https") and parsed.netloc
# # # # # def detect_browser(user_agent):

# # # # #     if not user_agent:
# # # # #         return "Unknown"

# # # # #     user_agent = user_agent.lower()

# # # # #     if "edg" in user_agent:
# # # # #         return "Edge"

# # # # #     elif "chrome" in user_agent:
# # # # #         return "Chrome"

# # # # #     elif "firefox" in user_agent:
# # # # #         return "Firefox"

# # # # #     elif "safari" in user_agent:
# # # # #         return "Safari"

# # # # #     else:
# # # # #         return "Unknown"
# # # # # app = Flask(__name__)

# # # # # @app.route("/")
# # # # # def home():

# # # # #     conn = get_db_connection()

# # # # #     conn.close()

# # # # #     return render_template("index.html")

# # # # # # if __name__ == "__main__":
# # # # # #     app.run(debug=True)
# # # # # # app = Flask(__name__)

# # # # # @app.route("/generate", methods=["POST"])
# # # # # def generate():

# # # # #     destination = request.form["url"]
# # # # #     if not valid_url(destination):
# # # # #      return "Invalid URL"

# # # # #     tracking_id = generate_tracking_id()

# # # # #     conn = get_db_connection()
# # # # #     print(f"Generated Tracking ID: {tracking_id} for Destination URL: {destination}")

# # # # #     cursor = conn.cursor()

# # # # #     cursor.execute("""

# # # # #     INSERT INTO links

# # # # #     (tracking_id,destination_url)

# # # # #     VALUES (?,?)

# # # # #     """,(tracking_id,destination))

# # # # #     conn.commit()

# # # # #     conn.close()

# # # # #     return f"""

# # # # # Tracking Link Created

# # # # # <br><br>

# # # # # Tracking ID : {tracking_id}

# # # # # <br><br>

# # # # # Tracking URL :

# # # # # <a href="/t/{tracking_id}">

# # # # # http://127.0.0.1:5000/t/{tracking_id}

# # # # # </a>

# # # # # """
# # # # # @app.route("/t/<tracking_id>")
# # # # # def track(tracking_id):

# # # # #     conn = get_db_connection()

# # # # #     cursor = conn.cursor()

# # # # #     cursor.execute(
# # # # #         "SELECT destination_url FROM links WHERE tracking_id=?",
# # # # #         (tracking_id,)
# # # # #     )

# # # # #     link = cursor.fetchone()

# # # # #     if not link:
# # # # #         conn.close()
# # # # #         return render_template("404.html"),404
# # # # #     destination = link["destination_url"]
# # # # #     ip = request.remote_addr

# # # # #     user_agent = request.headers.get("User-Agent")
# # # # #     browser = detect_browser(user_agent)
# # # # #     print("Browser =", browser)
# # # # #     print("User Agent =", user_agent)
# # # # #     referer = request.headers.get("Referer")
# # # # #     cursor.execute("""
# # # # # INSERT INTO clicks
# # # # # (tracking_id, ip_address, user_agent, browser, referer)
# # # # # VALUES (?, ?, ?, ?, ?)
# # # # # """, (tracking_id, ip, user_agent, browser, referer))

# # # # #     conn.commit()
# # # # #     conn.close()
# # # # #     return redirect(destination)
# # # # # # @app.route("/")
# # # # # # def home():
# # # # # #     return "Welcome to TraceRoute.io"
# # # # # @app.route("/analytics/<tracking_id>")
# # # # # def analytics(tracking_id):

# # # # #     conn = get_db_connection()
# # # # #     cursor = conn.cursor()

# # # # #     # Total Click Count
# # # # #     cursor.execute("""
# # # # #         SELECT COUNT(*) AS total_clicks
# # # # #         FROM clicks
# # # # #         WHERE tracking_id=?
# # # # #     """, (tracking_id,))

# # # # #     click_data = cursor.fetchone()

# # # # #     total_clicks = click_data["total_clicks"]
# # # # #     # Parent Tracking ID aur Generation

# # # # #     cursor.execute("""
# # # # # SELECT parent_tracking_id, generation
# # # # # FROM traversal_nodes
# # # # # WHERE tracking_id=?
# # # # # """, (tracking_id,))

# # # # #     tree_data = cursor.fetchone()

# # # # #     if tree_data:
# # # # #         parent_tracking = tree_data["parent_tracking_id"]
# # # # #         generation = tree_data["generation"]
# # # # #     else:
# # # # #         parent_tracking = "Original Link"
# # # # #         generation = 0
# # # # #     # Total Children Count

# # # # #     cursor.execute("""
# # # # # SELECT COUNT(*) AS total_children
# # # # # FROM traversal_nodes
# # # # # WHERE parent_tracking_id=?
# # # # # """, (tracking_id,))

# # # # #     child_data = cursor.fetchone()

# # # # #     total_children = child_data["total_children"]  
# # # # #      # Click History

# # # # #     cursor.execute("""
# # # # # SELECT ip_address, browser, clicked_at
# # # # # FROM clicks
# # # # # WHERE tracking_id=?
# # # # # ORDER BY clicked_at DESC
# # # # # """, (tracking_id,))

# # # # #     click_history = cursor.fetchall()
# # # # #     conn.close()
# # # # #     history_html = ""
 
# # # # #     for click in click_history:
# # # # #      history_html += f"""
# # # # #     <tr>
# # # # #         <td>{click['ip_address']}</td>
# # # # #         <td>{click['browser']}</td>
# # # # #         <td>{click['clicked_at']}</td>
# # # # #     </tr>
# # # # #     """
# # # # #      return render_template(

# # # # #     "analytics.html",

# # # # #     tracking_id=tracking_id,

# # # # #     total_clicks=total_clicks,

# # # # #     parent_tracking=parent_tracking,

# # # # #     generation=generation,

# # # # #     total_children=total_children,

# # # # #     click_history=click_history

# # # # # ) 

# # # # # @app.route("/share/<tracking_id>")
# # # # # def share(tracking_id):

# # # # #     conn = get_db_connection()
# # # # #     cursor = conn.cursor()

# # # # #     # Parent tracking link ko database me search karo
# # # # #     cursor.execute(
# # # # #         "SELECT destination_url FROM links WHERE tracking_id=?",
# # # # #         (tracking_id,)
# # # # #     )

# # # # #     link = cursor.fetchone()

# # # # #     # Agar tracking ID nahi mili
# # # # #     if not link:
# # # # #         conn.close()
# # # # #         return "Tracking Link Not Found"

# # # # #     # Original destination URL nikal lo
# # # # #     destination = link["destination_url"]
# # # # #     cursor.execute("""
# # # # #     SELECT generation
# # # # #     FROM traversal_nodes
# # # # #     WHERE tracking_id=?
# # # # #     """, (tracking_id,))

# # # # #     parent = cursor.fetchone()
# # # # #     if parent:
# # # # #         generation = parent["generation"] + 1
# # # # #     else:
# # # # #        generation = 1
# # # # #     child_tracking = generate_tracking_id()
# # # # #     cursor.execute("""
# # # # # INSERT INTO links
# # # # # (tracking_id, destination_url)
# # # # # VALUES (?, ?)
# # # # # """, (child_tracking, destination))
# # # # #     cursor.execute("""
# # # # # INSERT INTO traversal_nodes
# # # # # (tracking_id, parent_tracking_id, generation)
# # # # # VALUES (?, ?, ?)
# # # # # """, (child_tracking, tracking_id, generation))
# # # # #     conn.commit()
# # # # #     conn.close()

# # # # #     # Test ke liye sirf destination dikha rahe hain
# # # # #     return f"""
# # # # # <h2>Child Tracking Link Created</h2>

# # # # # <b>Parent Tracking ID:</b> {tracking_id}<br><br>

# # # # # <b>Child Tracking ID:</b> {child_tracking}<br><br>

# # # # # <b>Tracking Link:</b><br>

# # # # # <a href="/t/{child_tracking}">
# # # # # http://127.0.0.1:5000/t/{child_tracking}
# # # # # </a>
# # # # # """
# # # # # if __name__ == "__main__":
# #     #   app.run(debug=True)
# # from flask import Flask, render_template, request, redirect, jsonify
# # from database import get_db_connection
# # from utils.generator import generate_tracking_id
# # from urllib.parse import urlparse

# # app = Flask(__name__)


# # # ---------------- Helper Functions ----------------

# # def valid_url(url):
# #     parsed = urlparse(url)
# #     return parsed.scheme in ("http", "https") and parsed.netloc


# # def detect_browser(user_agent):
# #     if not user_agent:
# #         return "Unknown"

# #     user_agent = user_agent.lower()

# #     if "edg" in user_agent:
# #         return "Edge"
# #     elif "chrome" in user_agent:
# #         return "Chrome"
# #     elif "firefox" in user_agent:
# #         return "Firefox"
# #     elif "safari" in user_agent:
# #         return "Safari"
# #     else:
# #         return "Unknown"


# # # ---------------- Home Route ----------------

# # @app.route("/")
# # def home():
# #     return render_template("index.html")


# # # ---------------- Generate Tracking Link ----------------

# # @app.route("/generate", methods=["POST"])
# # def generate():
# #     destination = request.form["url"]

# #     if not valid_url(destination):
# #         return "Invalid URL"

# #     tracking_id = generate_tracking_id()

# #     conn = get_db_connection()
# #     cursor = conn.cursor()

# #     cursor.execute(
# #         """
# #         INSERT INTO links (tracking_id, destination_url)
# #         VALUES (?, ?)
# #         """,
# #         (tracking_id, destination),
# #     )

# #     conn.commit()
# #     conn.close()

# #     return f"""
# #     <h2>Tracking Link Created</h2>
# #     <b>Tracking ID:</b> {tracking_id}<br><br>
# #     <b>Tracking Link:</b><br>
# #     <a href="/t/{tracking_id}">
# #     http://127.0.0.1:5000/t/{tracking_id}
# #     </a>
# #     """


# # # ---------------- Track Route ----------------

# # @app.route("/t/<tracking_id>")
# # def track(tracking_id):
# #     conn = get_db_connection()
# #     cursor = conn.cursor()

# #     cursor.execute(
# #         "SELECT destination_url FROM links WHERE tracking_id=?",
# #         (tracking_id,),
# #     )

# #     link = cursor.fetchone()

# #     if not link:
# #         conn.close()
# #         return render_template("404.html"), 404

# #     destination = link["destination_url"]

# #     ip = request.remote_addr
# #     user_agent = request.headers.get("User-Agent")
# #     browser = detect_browser(user_agent)
# #     referer = request.headers.get("Referer")

# #     cursor.execute(
# #         """
# #         INSERT INTO clicks
# #         (tracking_id, ip_address, user_agent, browser, referer)
# #         VALUES (?, ?, ?, ?, ?)
# #         """,
# #         (tracking_id, ip, user_agent, browser, referer),
# #     )

# #     conn.commit()
# #     conn.close()

# #     return redirect(destination)


# # # ---------------- Analytics Route ----------------

# # @app.route("/analytics/<tracking_id>")
# # def analytics(tracking_id):
# #     conn = get_db_connection()
# #     cursor = conn.cursor()

# #     # Total Clicks
# #     cursor.execute(
# #         """
# #         SELECT COUNT(*) AS total_clicks
# #         FROM clicks
# #         WHERE tracking_id=?
# #         """,
# #         (tracking_id,),
# #     )
# #     click_data = cursor.fetchone()
# #     total_clicks = click_data["total_clicks"]

# #     # Parent Tracking ID and Generation
# #     cursor.execute(
# #         """
# #         SELECT parent_tracking_id, generation
# #         FROM traversal_nodes
# #         WHERE tracking_id=?
# #         """,
# #         (tracking_id,),
# #     )
# #     tree_data = cursor.fetchone()

# #     if tree_data:
# #         parent_tracking = tree_data["parent_tracking_id"]
# #         generation = tree_data["generation"]
# #     else:
# #         parent_tracking = "Original Link"
# #         generation = 0

# #     # Total Children
# #     cursor.execute(
# #         """
# #         SELECT COUNT(*) AS total_children
# #         FROM traversal_nodes
# #         WHERE parent_tracking_id=?
# #         """,
# #         (tracking_id,),
# #     )
# #     child_data = cursor.fetchone()
# #     total_children = child_data["total_children"]

# #     # Click History
# #     cursor.execute(
# #         """
# #         SELECT ip_address, browser, clicked_at
# #         FROM clicks
# #         WHERE tracking_id=?
# #         ORDER BY clicked_at DESC
# #         """,
# #         (tracking_id,),
# #     )
# #     click_history = cursor.fetchall()

# #     conn.close()

# #     return render_template(
# #         "analytics.html",
# #         tracking_id=tracking_id,
# #         total_clicks=total_clicks,
# #         parent_tracking=parent_tracking,
# #         generation=generation,
# #         total_children=total_children,
# #         click_history=click_history,
# #     )


# # # ---------------- Share Route ----------------

# # @app.route("/share/<tracking_id>")
# # def share(tracking_id):
# #     conn = get_db_connection()
# #     cursor = conn.cursor()

# #     cursor.execute(
# #         "SELECT destination_url FROM links WHERE tracking_id=?",
# #         (tracking_id,),
# #     )

# #     link = cursor.fetchone()

# #     if not link:
# #         conn.close()
# #         return "Tracking Link Not Found"

# #     destination = link["destination_url"]

# #     # Parent generation check
# #     cursor.execute(
# #         """
# #         SELECT generation
# #         FROM traversal_nodes
# #         WHERE tracking_id=?
# #         """,
# #         (tracking_id,),
# #     )

# #     parent = cursor.fetchone()

# #     if parent:
# #         generation = parent["generation"] + 1
# #     else:
# #         generation = 1

# #     child_tracking = generate_tracking_id()

# #     # Save child link
# #     cursor.execute(
# #         """
# #         INSERT INTO links (tracking_id, destination_url)
# #         VALUES (?, ?)
# #         """,
# #         (child_tracking, destination),
# #     )

# #     # Save parent-child relation
# #     cursor.execute(
# #         """
# #         INSERT INTO traversal_nodes
# #         (tracking_id, parent_tracking_id, generation)
# #         VALUES (?, ?, ?)
# #         """,
# #         (child_tracking, tracking_id, generation),
# #     )

# #     conn.commit()
# #     conn.close()

# #     return f"""
# #     <h2>Child Tracking Link Created</h2>
# #     <b>Parent Tracking ID:</b> {tracking_id}<br><br>
# #     <b>Child Tracking ID:</b> {child_tracking}<br><br>
# #     <b>Tracking Link:</b><br>
# #     <a href="/t/{child_tracking}">
# #     http://127.0.0.1:5000/t/{child_tracking}
# #     </a>
# #     """


# # # ---------------- Main ----------------

# # if __name__ == "__main__":
# #     app.run(debug=True)
# # from flask import Flask, render_template, request, redirect, jsonify
# # from database import get_db_connection
# # from utils.generator import generate_tracking_id
# # from urllib.parse import urlparse

# # def valid_url(url):
# # parsed = urlparse(url)
# # # #     return parsed.scheme in ("http", "https") and parsed.netloc
# # # # def detect_browser(user_agent):

# # # #     if not user_agent:
# # # #         return "Unknown"

# # # #     user_agent = user_agent.lower()

# # # #     if "edg" in user_agent:
# # # #         return "Edge"

# # # #     elif "chrome" in user_agent:
# # # #         return "Chrome"

# # # #     elif "firefox" in user_agent:
# # # #         return "Firefox"

# # # #     elif "safari" in user_agent:
# # # #         return "Safari"

# # # #     else:
# # # #         return "Unknown"
# # # # app = Flask(__name__)

# # # # @app.route("/")
# # # # def home():

# # # #     conn = get_db_connection()

# # # #     conn.close()

# # # #     return render_template("index.html")

# # # # # if __name__ == "__main__":
# # # # #     app.run(debug=True)
# # # # # app = Flask(__name__)

# # # # @app.route("/generate", methods=["POST"])
# # # # def generate():

# # # #     destination = request.form["url"]
# # # #     if not valid_url(destination):
# # # #      return "Invalid URL"

# # # #     tracking_id = generate_tracking_id()

# # # #     conn = get_db_connection()
# # # #     print(f"Generated Tracking ID: {tracking_id} for Destination URL: {destination}")

# # # #     cursor = conn.cursor()

# # # #     cursor.execute("""

# # # #     INSERT INTO links

# # # #     (tracking_id,destination_url)

# # # #     VALUES (?,?)

# # # #     """,(tracking_id,destination))

# # # #     conn.commit()

# # # #     conn.close()

# # # #     return f"""

# # # # Tracking Link Created

# # # # <br><br>

# # # # Tracking ID : {tracking_id}

# # # # <br><br>

# # # # Tracking URL :

# # # # <a href="/t/{tracking_id}">

# # # # http://127.0.0.1:5000/t/{tracking_id}

# # # # </a>

# # # # """
# # # # @app.route("/t/<tracking_id>")
# # # # def track(tracking_id):

# # # #     conn = get_db_connection()

# # # #     cursor = conn.cursor()

# # # #     cursor.execute(
# # # #         "SELECT destination_url FROM links WHERE tracking_id=?",
# # # #         (tracking_id,)
# # # #     )

# # # #     link = cursor.fetchone()

# # # #     if not link:
# # # #         conn.close()
# # # #         return render_template("404.html"),404
# # # #     destination = link["destination_url"]
# # # #     ip = request.remote_addr

# # # #     user_agent = request.headers.get("User-Agent")
# # # #     browser = detect_browser(user_agent)
# # # #     print("Browser =", browser)
# # # #     print("User Agent =", user_agent)
# # # #     referer = request.headers.get("Referer")
# # # #     cursor.execute("""
# # # # INSERT INTO clicks
# # # # (tracking_id, ip_address, user_agent, browser, referer)
# # # # VALUES (?, ?, ?, ?, ?)
# # # # """, (tracking_id, ip, user_agent, browser, referer))

# # # #     conn.commit()
# # # #     conn.close()
# # # #     return redirect(destination)
# # # # # @app.route("/")
# # # # # def home():
# # # # #     return "Welcome to TraceRoute.io"
# # # # @app.route("/analytics/<tracking_id>")
# # # # def analytics(tracking_id):

# # # #     conn = get_db_connection()
# # # #     cursor = conn.cursor()

# # # #     # Total Click Count
# # # #     cursor.execute("""
# # # #         SELECT COUNT(*) AS total_clicks
# # # #         FROM clicks
# # # #         WHERE tracking_id=?
# # # #     """, (tracking_id,))

# # # #     click_data = cursor.fetchone()

# # # #     total_clicks = click_data["total_clicks"]
# # # #     # Parent Tracking ID aur Generation

# # # #     cursor.execute("""
# # # # SELECT parent_tracking_id, generation
# # # # FROM traversal_nodes
# # # # WHERE tracking_id=?
# # # # """, (tracking_id,))

# # # #     tree_data = cursor.fetchone()

# # # #     if tree_data:
# # # #         parent_tracking = tree_data["parent_tracking_id"]
# # # #         generation = tree_data["generation"]
# # # #     else:
# # # #         parent_tracking = "Original Link"
# # # #         generation = 0
# # # #     # Total Children Count

# # # #     cursor.execute("""
# # # # SELECT COUNT(*) AS total_children
# # # # FROM traversal_nodes
# # # # WHERE parent_tracking_id=?
# # # # """, (tracking_id,))

# # # #     child_data = cursor.fetchone()

# # # #     total_children = child_data["total_children"]  
# # # #      # Click History

# # # #     cursor.execute("""
# # # # SELECT ip_address, browser, clicked_at
# # # # FROM clicks
# # # # WHERE tracking_id=?
# # # # ORDER BY clicked_at DESC
# # # # """, (tracking_id,))

# # # #     click_history = cursor.fetchall()
# # # #     conn.close()
# # # #     history_html = ""
 
# # # #     for click in click_history:
# # # #      history_html += f"""
# # # #     <tr>
# # # #         <td>{click['ip_address']}</td>
# # # #         <td>{click['browser']}</td>
# # # #         <td>{click['clicked_at']}</td>
# # # #     </tr>
# # # #     """
# # # #      return render_template(

# # # #     "analytics.html",

# # # #     tracking_id=tracking_id,

# # # #     total_clicks=total_clicks,

# # # #     parent_tracking=parent_tracking,

# # # #     generation=generation,

# # # #     total_children=total_children,

# # # #     click_history=click_history

# # # # ) 

# # # # @app.route("/share/<tracking_id>")
# # # # def share(tracking_id):

# # # #     conn = get_db_connection()
# # # #     cursor = conn.cursor()

# # # #     # Parent tracking link ko database me search karo
# # # #     cursor.execute(
# # # #         "SELECT destination_url FROM links WHERE tracking_id=?",
# # # #         (tracking_id,)
# # # #     )

# # # #     link = cursor.fetchone()

# # # #     # Agar tracking ID nahi mili
# # # #     if not link:
# # # #         conn.close()
# # # #         return "Tracking Link Not Found"

# # # #     # Original destination URL nikal lo
# # # #     destination = link["destination_url"]
# # # #     cursor.execute("""
# # # #     SELECT generation
# # # #     FROM traversal_nodes
# # # #     WHERE tracking_id=?
# # # #     """, (tracking_id,))

# # # #     parent = cursor.fetchone()
# # # #     if parent:
# # # #         generation = parent["generation"] + 1
# # # #     else:
# # # #        generation = 1
# # # #     child_tracking = generate_tracking_id()
# # # #     cursor.execute("""
# # # # INSERT INTO links
# # # # (tracking_id, destination_url)
# # # # VALUES (?, ?)
# # # # """, (child_tracking, destination))
# # # #     cursor.execute("""
# # # # INSERT INTO traversal_nodes
# # # # (tracking_id, parent_tracking_id, generation)
# # # # VALUES (?, ?, ?)
# # # # """, (child_tracking, tracking_id, generation))
# # # #     conn.commit()
# # # #     conn.close()

# # # #     # Test ke liye sirf destination dikha rahe hain
# # # #     return f"""
# # # # <h2>Child Tracking Link Created</h2>

# # # # <b>Parent Tracking ID:</b> {tracking_id}<br><br>

# # # # <b>Child Tracking ID:</b> {child_tracking}<br><br>

# # # # <b>Tracking Link:</b><br>

# # # # <a h    #   app.run(debug=True)
# ref="/t/{child_tracking}">
# # # # http://127.0.0.1:5000/t/{child_tracking}
# # # # </a>
# # # # """
# # # # if __name__ == "__main__":
# from flask import Flask, render_template, request, redirect, jsonify
# from database import get_db_connection
# from utils.generator import generate_tracking_id
# from urllib.parse import urlparse

# app = Flask(__name__)


# # ---------------- Helper Functions ----------------

# def valid_url(url):
#     parsed = urlparse(url)
#     return parsed.scheme in ("http", "https") and parsed.netloc


# def detect_browser(user_agent):
#     if not user_agent:
#         return "Unknown"

#     user_agent = user_agent.lower()

#     if "edg" in user_agent:
#         return "Edge"
#     elif "chrome" in user_agent:
#         return "Chrome"
#     elif "firefox" in user_agent:
#         return "Firefox"
#     elif "safari" in user_agent:
#         return "Safari"
#     else:
#         return "Unknown"


# def get_click_count(cursor, tracking_id):
#     cursor.execute("SELECT COUNT(*) AS c FROM clicks WHERE tracking_id=?", (tracking_id,))
#     return cursor.fetchone()["c"]


# def find_root(cursor, tracking_id):
#     """Walks up the parent chain until it hits the original (root) link."""
#     current = tracking_id
#     while True:
#         cursor.execute(
#             "SELECT parent_tracking_id FROM traversal_nodes WHERE tracking_id=?",
#             (current,),
#         )
#         row = cursor.fetchone()
#         if row and row["parent_tracking_id"]:
#             current = row["parent_tracking_id"]
#         else:
#             break
#     return current


# def build_tree(cursor, tracking_id, generation=0):
#     """Recursively builds the full forwarding tree starting at tracking_id."""
#     node = {
#         "tracking_id": tracking_id,
#         "generation": generation,
#         "clicks": get_click_count(cursor, tracking_id),
#         "children": [],
#     }
#     cursor.execute(
#         "SELECT tracking_id FROM traversal_nodes WHERE parent_tracking_id=? ORDER BY tracking_id",
#         (tracking_id,),
#     )
#     for row in cursor.fetchall():
#         node["children"].append(build_tree(cursor, row["tracking_id"], generation + 1))
#     return node


# # ---------------- Home Route ----------------

# @app.route("/")
# def home():
#     return render_template("index.html")


# # ---------------- Generate Tracking Link ----------------

# @app.route("/generate", methods=["POST"])
# def generate():
#     destination = request.form["url"]

#     if not valid_url(destination):
#         return "Invalid URL"

#     tracking_id = generate_tracking_id()

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute(
#         """
#         INSERT INTO links (tracking_id, destination_url)
#         VALUES (?, ?)
#         """,
#         (tracking_id, destination),
#     )

#     conn.commit()
#     conn.close()

#     return jsonify({
#         "tracking_id": tracking_id,
#         "short_url": request.host_url.rstrip("/") + f"/t/{tracking_id}"
#     })


# # ---------------- Track Route ----------------

# @app.route("/t/<tracking_id>")
# def track(tracking_id):
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute(
#         "SELECT destination_url FROM links WHERE tracking_id=?",
#         (tracking_id,),
#     )

#     link = cursor.fetchone()

#     if not link:
#         conn.close()
#         return render_template("404.html"), 404

#     destination = link["destination_url"]

#     ip = request.remote_addr
#     user_agent = request.headers.get("User-Agent")
#     browser = detect_browser(user_agent)
#     referer = request.headers.get("Referer")

#     cursor.execute(
#         """
#         INSERT INTO clicks
#         (tracking_id, ip_address, user_agent, browser, referer)
#         VALUES (?, ?, ?, ?, ?)
#         """,
#         (tracking_id, ip, user_agent, browser, referer),
#     )

#     conn.commit()
#     conn.close()

#     return redirect(destination)


# # ---------------- Analytics Route ----------------

# @app.route("/analytics/<tracking_id>")
# def analytics(tracking_id):
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     # Total Clicks
#     cursor.execute(
#         """
#         SELECT COUNT(*) AS total_clicks
#         FROM clicks
#         WHERE tracking_id=?
#         """,
#         (tracking_id,),
#     )
#     click_data = cursor.fetchone()
#     total_clicks = click_data["total_clicks"]

#     # Parent Tracking ID and Generation
#     cursor.execute(
#         """
#         SELECT parent_tracking_id, generation
#         FROM traversal_nodes
#         WHERE tracking_id=?
#         """,
#         (tracking_id,),
#     )
#     tree_data = cursor.fetchone()

#     if tree_data:
#         parent_tracking = tree_data["parent_tracking_id"]
#         generation = tree_data["generation"]
#     else:
#         parent_tracking = "Original Link"
#         generation = 0

#     # Total Children
#     cursor.execute(
#         """
#         SELECT COUNT(*) AS total_children
#         FROM traversal_nodes
#         WHERE parent_tracking_id=?
#         """,
#         (tracking_id,),
#     )
#     child_data = cursor.fetchone()
#     total_children = child_data["total_children"]

#     # Click History
#     cursor.execute(
#         """
#         SELECT ip_address, browser, clicked_at
#         FROM clicks
#         WHERE tracking_id=?
#         ORDER BY clicked_at DESC
#         """,
#         (tracking_id,),
#     )
#     click_history = cursor.fetchall()

#     # Full forwarding tree — walk up to the root link, then build the tree back down
#     root_id = find_root(cursor, tracking_id)
#     tree_data = build_tree(cursor, root_id)

#     conn.close()

#     return render_template(
#         "analytics.html",
#         tracking_id=tracking_id,
#         total_clicks=total_clicks,
#         parent_tracking=parent_tracking,
#         generation=generation,
#         total_children=total_children,
#         click_history=click_history,
#         tree_data=tree_data,
#     )


# # ---------------- Share Route ----------------

# @app.route("/share/<tracking_id>")
# def share(tracking_id):
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute(
#         "SELECT destination_url FROM links WHERE tracking_id=?",
#         (tracking_id,),
#     )

#     link = cursor.fetchone()

#     if not link:
#         conn.close()
#         return "Tracking Link Not Found"

#     destination = link["destination_url"]

#     # Parent generation check
#     cursor.execute(
#         """
#         SELECT generation
#         FROM traversal_nodes
#         WHERE tracking_id=?
#         """,
#         (tracking_id,),
#     )

#     parent = cursor.fetchone()

#     if parent:
#         generation = parent["generation"] + 1
#     else:
#         generation = 1

#     child_tracking = generate_tracking_id()

#     # Save child link
#     cursor.execute(
#         """
#         INSERT INTO links (tracking_id, destination_url)
#         VALUES (?, ?)
#         """,
#         (child_tracking, destination),
#     )

#     # Save parent-child relation
#     cursor.execute(
#         """
#         INSERT INTO traversal_nodes
#         (tracking_id, parent_tracking_id, generation)
#         VALUES (?, ?, ?)
#         """,
#         (child_tracking, tracking_id, generation),
#     )

#     conn.commit()
#     conn.close()

#     return f"""
#     <h2>Child Tracking Link Created</h2>
#     <b>Parent Tracking ID:</b> {tracking_id}<br><br>
#     <b>Child Tracking ID:</b> {child_tracking}<br><br>
#     <b>Tracking Link:</b><br>
#     <a href="/t/{child_tracking}">
#     http://127.0.0.1:5000/t/{child_tracking}
#     </a>
#     """


# # ---------------- Main ----------------

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5000)
from flask import Flask, render_template, request, redirect, jsonify
from database import get_db_connection
from utils.generator import generate_tracking_id
from urllib.parse import urlparse

app = Flask(__name__)


# ---------------- Helper Functions ----------------

def valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and parsed.netloc


def detect_browser(user_agent):
    if not user_agent:
        return "Unknown"

    user_agent = user_agent.lower()

    if "edg" in user_agent:
        return "Edge"
    elif "chrome" in user_agent:
        return "Chrome"
    elif "firefox" in user_agent:
        return "Firefox"
    elif "safari" in user_agent:
        return "Safari"
    else:
        return "Unknown"


def get_click_count(cursor, tracking_id):
    cursor.execute("SELECT COUNT(*) AS c FROM clicks WHERE tracking_id=?", (tracking_id,))
    return cursor.fetchone()["c"]


def find_root(cursor, tracking_id):
    """Walks up the parent chain until it hits the original (root) link."""
    current = tracking_id
    while True:
        cursor.execute(
            "SELECT parent_tracking_id FROM traversal_nodes WHERE tracking_id=?",
            (current,),
        )
        row = cursor.fetchone()
        if row and row["parent_tracking_id"]:
            current = row["parent_tracking_id"]
        else:
            break
    return current


def build_tree(cursor, tracking_id, generation=0):
    """Recursively builds the full forwarding tree starting at tracking_id."""
    node = {
        "tracking_id": tracking_id,
        "generation": generation,
        "clicks": get_click_count(cursor, tracking_id),
        "children": [],
    }
    cursor.execute(
        "SELECT tracking_id FROM traversal_nodes WHERE parent_tracking_id=? ORDER BY tracking_id",
        (tracking_id,),
    )
    for row in cursor.fetchall():
        node["children"].append(build_tree(cursor, row["tracking_id"], generation + 1))
    return node


# ---------------- Home Route ----------------

@app.route("/links")
def all_links():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT tracking_id, destination_url, created_at FROM links ORDER BY created_at DESC"
    )
    rows = cursor.fetchall()

    links_list = []
    for row in rows:
        tid = row["tracking_id"]
        cursor.execute("SELECT COUNT(*) AS c FROM clicks WHERE tracking_id=?", (tid,))
        total_clicks = cursor.fetchone()["c"]
        cursor.execute("SELECT COUNT(*) AS c FROM traversal_nodes WHERE parent_tracking_id=?", (tid,))
        total_children = cursor.fetchone()["c"]
        links_list.append({
            "tracking_id": tid,
            "destination_url": row["destination_url"],
            "created_at": row["created_at"],
            "total_clicks": total_clicks,
            "total_children": total_children,
        })

    conn.close()
    return render_template("links.html", links=links_list)


@app.route("/")
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT max(id) AS c FROM clicks")
    all_clicks = cursor.fetchone()["c"]

    cursor.execute("SELECT COUNT(DISTINCT ip_address) AS unique_ip from clicks")
    unique_ips = cursor.fetchone()["unique_ip"]

    cursor.execute("SELECT COUNT(DISTINCT tracking_id) AS active_link from clicks")
    active_links = cursor.fetchone()["active_link"]
    
    return render_template("index.html", all_clicks=all_clicks, unique_ips=unique_ips, active_links=active_links)


# ---------------- Generate Tracking Link ----------------

@app.route("/generate", methods=["POST"])
def generate():
    destination = request.form["url"]

    if not valid_url(destination):
        return jsonify({"error": "Invalid URL"}), 400

    tracking_id = generate_tracking_id()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO links (tracking_id, destination_url)
        VALUES (?, ?)
        """,
        (tracking_id, destination),
    )

    conn.commit()
    conn.close()

    return jsonify({
        "tracking_id": tracking_id,
        "short_url": request.host_url.rstrip("/") + f"/t/{tracking_id}"
    })


# ---------------- Track Route (this is the redirect + click logger) ----------------

@app.route("/t/<tracking_id>")
def track(tracking_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT destination_url FROM links WHERE tracking_id=?",
        (tracking_id,),
    )
    link = cursor.fetchone()

    if not link:
        conn.close()
        return render_template("404.html"), 404

    destination = link["destination_url"]

    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent")
    browser = detect_browser(user_agent)
    referer = request.headers.get("Referer")

    cursor.execute(
        """
        INSERT INTO clicks
        (tracking_id, ip_address, user_agent, browser, referer)
        VALUES (?, ?, ?, ?, ?)
        """,
        (tracking_id, ip, user_agent, browser, referer),
    )

    conn.commit()
    conn.close()

    return redirect(destination)


# ---------------- Analytics Route ----------------

@app.route("/analytics/<tracking_id>")
def analytics(tracking_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Make sure the tracking ID actually exists before building a whole page for it
    cursor.execute("SELECT tracking_id FROM links WHERE tracking_id=?", (tracking_id,))
    if not cursor.fetchone():
        conn.close()
        return render_template("404.html"), 404

    # Total clicks for this specific link
    cursor.execute(
        "SELECT COUNT(*) AS total_clicks FROM clicks WHERE tracking_id=?",
        (tracking_id,),
    )
    total_clicks = cursor.fetchone()["total_clicks"]

    # Parent tracking ID and generation
    cursor.execute(
        "SELECT parent_tracking_id, generation FROM traversal_nodes WHERE tracking_id=?",
        (tracking_id,),
    )
    parent_row = cursor.fetchone()

    if parent_row:
        parent_tracking = parent_row["parent_tracking_id"]
        generation = parent_row["generation"]
    else:
        parent_tracking = "Original Link"
        generation = 0

    # Total direct children of this link
    cursor.execute(
        "SELECT COUNT(*) AS total_children FROM traversal_nodes WHERE parent_tracking_id=?",
        (tracking_id,),
    )
    total_children = cursor.fetchone()["total_children"]

    # Click history for this specific link
    cursor.execute(
        """
        SELECT ip_address, browser, clicked_at
        FROM clicks
        WHERE tracking_id=?
        ORDER BY clicked_at DESC
        """,
        (tracking_id,),
    )
    click_history = cursor.fetchall()

    # Full forwarding tree — walk up to the original root link, then build the whole tree back down
    root_id = find_root(cursor, tracking_id)
    tree_data = build_tree(cursor, root_id)

    conn.close()

    return render_template(
        "analytics.html",
        tracking_id=tracking_id,
        total_clicks=total_clicks,
        parent_tracking=parent_tracking,
        generation=generation,
        total_children=total_children,
        click_history=click_history,
        tree_data=tree_data,
    )


# ---------------- Share Route (creates a forwarded child link) ----------------

@app.route("/share/<tracking_id>")
def share(tracking_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT destination_url FROM links WHERE tracking_id=?",
        (tracking_id,),
    )
    link = cursor.fetchone()

    if not link:
        conn.close()
        return render_template("404.html"), 404

    destination = link["destination_url"]

    cursor.execute(
        "SELECT generation FROM traversal_nodes WHERE tracking_id=?",
        (tracking_id,),
    )
    parent = cursor.fetchone()
    generation = (parent["generation"] + 1) if parent else 1

    child_tracking = generate_tracking_id()

    cursor.execute(
        "INSERT INTO links (tracking_id, destination_url) VALUES (?, ?)",
        (child_tracking, destination),
    )
    cursor.execute(
        """
        INSERT INTO traversal_nodes (tracking_id, parent_tracking_id, generation)
        VALUES (?, ?, ?)
        """,
        (child_tracking, tracking_id, generation),
    )

    conn.commit()
    conn.close()

    return jsonify({
        "parent_tracking_id": tracking_id,
        "tracking_id": child_tracking,
        "short_url": request.host_url.rstrip("/") + f"/t/{child_tracking}"
    })


# ---------------- Main ----------------

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)