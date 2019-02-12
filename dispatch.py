#!/user/bin/python
#-*-coding: utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from flask import Flask, Response, make_response, url_for, render_template, request, session, redirect
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.debug = True

@app.route("/user/<uname>")
def IoT_user_name(uname):
	return "User Name : %s" % uname

@app.route("/user/<int:num_id>")
def IoT_user_number_id(num_id):
	return "ID Number : %d" % num_id

@app.route("/log")
def IoT_logging_test():
	test_value = 20190211
	app.logger.debug("����� ���� ��")
	app.logger.warning(str(test_value) + "====")
	app.logger.error("�����߻�")
	return "�ΰ� ��"

@app.route("/get_test", methods=["GET"])
def get_test():
	if request.method == "GET":
		if (request.args.get("uname") == "iot"
				and request.args.get("passwd") == "2019"):
			return request.args.get("uname") + "ȯ���մϴ�."
		else :
			return "�α��� ����"
	else:
		return "�ٽ� �õ��� �ּ���"

@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		session_check = request.form.get("uname", None)
		if None == session_check:
			if "logged_in" in session:
				if True == session["logged_in"]:
					return session["uname"] + " welcome"
			return login_test()

		if request.form["uname"] == "iot":
			if request.form["passwd"] == "2019":
				session["logged_in"] = True
				session["uname"] = request.form["uname"]
				return request.form["uname"] + " welcome"
			else:
				return "login fail"
	else:
		if "logged_in" in session:
			if True == session["logged_in"]:
				return session["uname"] + " welcome"
		return login_test() 

app.secret_key = "iot_key"

@app.route("/logout")
def logout():
	session["logged_in"] = False
	session.pop("uname", None)
	return "logout"

@app.route("/login_test")
def login_test():
	return render_template('login.html')

@app.route('/board', methods=['GET'])
#def IoT_Board():
def board_list_get():
#	return "<img src=\"https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png\">"
	return "GET"

@app.route('/board', methods=['POST'])
def board_list_post():
	return "POST"

@app.route("/")
def IoT_http_prepost_response():
	return "<img src=" + url_for("static", filename = "1.jpg") + ">"

@app.route("/template")
@app.route("/template/")
@app.route("/template/<iot_number>")
def template_test(iot_number=None):
	iot_members = ["CHOI", "JOO", "CHOI2", "KANG"]
	return render_template("template_test.html", iot_number=iot_number, iot_members=iot_members)

@app.route("/iot")
@app.route("/iot/")
def iot():
	result_req	 = requests.get("http://busanit.ac.kr/p/?j=41")
	result_txt	 = result_req.text
	result_head	 = result_req.headers
	result_status = result_req.status_code
	if True == result_req.ok:
		obj_soup = BeautifulSoup(result_txt, "html.parser")
		iot_data = obj_soup.select("table.ej-tbl>tbody>tr>td>a")
		return render_template("main.html", iot_data = iot_data)
	else:
		return "Loading fail"

@app.route("/gugu")
@app.route("/gugu/")
@app.route("/gugu/<int:iot_num>")
def iot_gugu(iot_num=None):
	return render_template("gugu.html", iot_num=iot_num)

@app.route("/calcul", methods=["POST"])
def calcul(iot_num=None):
	if request.method == "POST":
		if "" == request.form["iot_num"]:
			cal_num = None
		else:
			cal_num = request.form["iot_num"]
	else:
		cal_num = None
	return redirect(url_for("iot_gugu", iot_num=cal_num))

if __name__ == "__main__":
	app.run(host = "192.168.0.203")

