from threading import Thread

import flask

app: flask.Flask = flask.Flask("")


@app.route("/")
def home():
    return flask.render_template("index.html")


@app.route("/gatcha")
def gatcha():
    SSR_input = flask.request.args.get("SSR_input", default=0, type=int)
    SR_input = flask.request.args.get("SR_input", default=0, type=int)
    R_input = flask.request.args.get("R_input", default=0, type=int)
    N_input = flask.request.args.get("N_input", default=0, type=int)
    one = flask.request.args.get(
        "one",
        default=None,
    )
    ten = flask.request.args.get(
        "ten",
        default=None,
    )
    if one is not None:
        gatcha_time = 1
    elif ten is not None:
        gatcha_time = 10
    else:
        return flask.render_template("result.html", title="錯誤", result="抽卡次數錯誤")

    import random

    SSR = int(SSR_input)
    SR = int(SR_input)
    R = int(R_input)
    N = int(N_input)

    if SSR + SR + R + N != 100:
        return flask.render_template("result.html", result="機率加總不等於100", title="錯誤")

    SSR_num = list(range(1, SSR + 1))
    SR_num = list(range(SSR + 1, SSR + SR + 1))
    R_num = list(range(SSR + SR + 1, SSR + SR + R + 1))
    N_num = list(range(SSR + SR + R + 1, SSR + SR + R + N + 1))
    gatcha_list = []
    for i in range(gatcha_time):
        print(f"第{i + 1}抽")
        gatcha = random.randint(1, SSR + SR + R + N)
        if gatcha in SSR_num:
            gatcha_list.append("SSR")
        elif gatcha in SR_num:
            gatcha_list.append("SR")
        elif gatcha in R_num:
            gatcha_list.append("R")
        else:
            gatcha_list.append("N")
    res = " ,".join(gatcha_list)
    return flask.render_template("result.html", result=res, title="結果")


def run():
    app.run()


def alive():
    t = Thread(target=run)
    t.start()


if __name__ == "__main__":
    alive()
