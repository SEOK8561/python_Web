#!/user/bin/python
#-*-coding: utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from flask import Flask, Response, make_response, url_for, render_template, request, session

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
	app.logger.debug("디버깅 시행 중")
	app.logger.warning(str(test_value) + "====")
	app.logger.error("에러발생")
	return "로거 끝"

@app.route("/get_test", methods=["GET"])
def get_test():
	if request.method == "GET":
		if (request.args.get("uname") == "iot"
				and request.args.get("passwd") == "2019"):
			return request.args.get("uname") + "환영합니다."
		else :
			return "로그인 실패"
	else:
		return "다시 시도해 주세요"

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

if __name__ == "__main__":
	app.run(host = "192.168.0.203")

