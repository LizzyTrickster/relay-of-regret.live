import functools

from flask import Flask, render_template
from flask_frozen import Freezer
from datetime import datetime, timezone, timedelta
app = Flask(__name__)

now = functools.partial(datetime.now, tz=timezone.utc)


@app.route("/")
def hello():
    start_date = datetime.fromtimestamp(1662138000, tz=timezone.utc)
    charity_list = [
        dict(img="https://relay-of-regret.live/static/trans-lifeline.png", url="trans-lifeline", slot=start_date+timedelta(days=4)),
        dict(img="https://relay-of-regret.live/static/acon.png", url="acon", slot=start_date+timedelta(days=2)),
        dict(img="https://relay-of-regret.live/static/euro-pride.png", url="europride", slot=start_date+timedelta(days=6)),
        dict(img="https://relay-of-regret.live/static/special-effect.png", url="special-effect", slot=start_date+timedelta(days=7)),
        dict(img="https://relay-of-regret.live/static/mermaids.png", url="mermaids", slot=start_date+timedelta(days=5)),
        dict(img="https://relay-of-regret.live/static/rescue.png", url="rescue.org", slot=start_date+timedelta(days=1)),
        dict(img="https://relay-of-regret.live/static/nqapia.png", url="nqapia", slot=start_date+timedelta(days=3)),
        dict(img="https://relay-of-regret.live/static/op-sun-kid.png", url="op-sun-kid", slot=start_date),
    ]
    timeslots = [
        (start_date, "BardicRJ", 12),
        (start_date + timedelta(hours=12), "WoodyWoodpie", 12),
        (start_date + timedelta(days=1), "sledgelp", 12),
        (start_date + timedelta(days=1.5), "merlekoz", 12),
        (start_date + timedelta(days=2), "moss", 12),
        (start_date + timedelta(days=2.5), "featheredflint", 12),
        (start_date + timedelta(days=3), "heartw00d", 12),
        (start_date + timedelta(days=3.5), "wishdream", 12),
        (start_date + timedelta(days=4), "nateybeak", 12),
        (start_date + timedelta(days=4.5), "silvixen", 6),
        (start_date + timedelta(days=4.75), "megasarts", 6),
        (start_date + timedelta(days=5), "leonfoxy", 12),
        (start_date + timedelta(days=5.5), "nanukk", 12),
        (start_date + timedelta(days=6), "kaideart", 12),
        (start_date + timedelta(days=6.5), "tygre", 12),
        (start_date + timedelta(days=7), "BardicRJ", 12),
        (start_date + timedelta(days=7.5), "WoodyWoodpie", 12),


    ]
    current_streamer = None
    current_charity = None
    for startdate, streamer, slot_hours in timeslots:
        if startdate < now() < startdate+timedelta(hours=slot_hours):
            current_streamer = streamer
            break
    for charity in charity_list:
        if charity['slot'] < now() < charity['slot']+timedelta(days=1):
            current_charity = charity
            break
    return render_template("index.html", charities=charity_list, timeslots=timeslots, now=now(), timedelta=timedelta,
                           current_streamer=current_streamer, current_charity=current_charity)


app.config["FREEZER_RELATIVE_URLS"] = True

freezer = Freezer(app)

if __name__ == "__main__":
    freezer.freeze()
    # app.run()
