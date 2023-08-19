import functools

import json, datetime
from collections import namedtuple
from dataclasses import dataclass
from flask import Flask, render_template, Response, request
from flask_frozen import Freezer
from celery import Celery, Task
from datetime import datetime, timezone, timedelta
import random

app = Flask(__name__)


@dataclass
class Campaign:
    """Holds Campaign info"""
    id: str
    total_raised: float = 0.0


@dataclass
class Charity:
    """Holds charity info"""
    name: str
    url: str
    img: str
    slot: datetime
    wilddogs_campaign: Campaign
    antlers_campaign: Campaign
    outlanders_campaign: Campaign
    currency: str = "US$"

    def total_raised(self) -> float:
        total =  self.wilddogs_campaign.total_raised + self.antlers_campaign.total_raised + self.outlanders_campaign.total_raised
        return total

currency_map = dict(USD="US$", EUR="€", GBP="£", AUD="AU$", CAD="CA$")

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


now = functools.partial(datetime.now, tz=timezone.utc)


lifetime_data = dict(grand_total=0.0)
start_date = datetime.fromtimestamp(1692378000, tz=timezone.utc)
# start_date = datetime.now(tz=timezone.utc) - timedelta(hours=13)
charity_list = [
    Charity(name="LGBT Foundation", url="2023-lgbt-foundation", img="img/lgbt-foundation.png", slot=start_date,
            wilddogs_campaign=Campaign("b5cb3b87-e9fd-4305-84b1-0520fa1aa12e"),
            antlers_campaign=Campaign("5274ee09-40d9-4bf3-a5e8-5e58cdbd5919"),
            outlanders_campaign=Campaign("f3e62a26-0e53-40a8-82d6-25a0bce72a3d"),
            currency=currency_map['GBP']
            ),
    Charity(name="EuroPride", url="2023-europride", img="img/europride.png", slot=start_date+timedelta(days=1),
            wilddogs_campaign=Campaign("88d2a01c-7c43-49c3-b507-05635818563a"),
            antlers_campaign=Campaign("6d503646-2fd0-4ec2-9160-eceadb2a9183"),
            outlanders_campaign=Campaign("5f0221ed-94c0-4825-86db-8119afe53ffb"),
            currency=currency_map['EUR']
            ),
    Charity(name="American Foundation for Suicide Prevention", url="2023-afsp", img="img/afsp.jpg", slot=start_date+timedelta(days=2),
            wilddogs_campaign=Campaign("79b4d5fe-38c6-4807-9ead-c82d4398386c"),
            antlers_campaign=Campaign("a887aef2-47c8-40dd-9bc3-6ae2f774538c"),
            outlanders_campaign=Campaign("35a1de40-41c6-4927-b1b9-ff6d21565591")
            ),
    Charity(name="National Queer Asian Pacific Islander Alliance", url="2023-nqapia", img="img/nqapia.png", slot=start_date+timedelta(days=3),
            wilddogs_campaign=Campaign("78f7e5fd-1fc8-4192-b22c-41c9e54dd9af"),
            antlers_campaign=Campaign("7c678737-07c8-4741-be48-75c280549c1c"),
            outlanders_campaign=Campaign("ce81de0e-fe5f-4177-ba0b-c0f1a6904513")
            ),
    Charity(name="ACON Health Limited", url="2023-acon", img="img/acon.png", slot=start_date+timedelta(days=4),
            wilddogs_campaign=Campaign("d5ee6898-7221-4495-b7a7-40a9c5824b2d"),
            antlers_campaign=Campaign("6c76b1d0-b595-427b-9062-a29ca3c43b90"),
            outlanders_campaign=Campaign("481bef99-64d8-4629-a611-bf99bfcafa51"),
            currency=currency_map['AUD']
            ),
    Charity(name="Trans Lifeline", url="2023-trans-lifeline", img="img/trans-lifeline.png", slot=start_date+timedelta(days=5),
            wilddogs_campaign=Campaign("b86c06be-971c-4eb1-8fb1-29057c4e1ac1"),
            antlers_campaign=Campaign("de6a9883-8363-4623-a459-8c007dc8576e"),
            outlanders_campaign=Campaign("f8ac38cd-b077-480f-a380-5db9f3a2cce0")
            ),
    Charity(name="GRIS Montreal", url="2023-gris-montreal", img="img/gris-montreal.png", slot=start_date+timedelta(days=6),
            wilddogs_campaign=Campaign("6ad15224-478d-42ac-923e-9cf79b67ea2d"),
            antlers_campaign=Campaign("075d4eb6-696d-4715-8d2f-e213eb697207"),
            outlanders_campaign=Campaign("7a2b5bfc-8e6e-4329-a3f6-c0f6b887e7c6"),
            currency=currency_map['CAD']
            )
]


@app.route("/")
def hello():

    timeslots = [
            (start_date, ("BardicRJ", "ItsMapleDoe"), 12),  # Friday PM
            (start_date + timedelta(hours=12), ("kitlantro", "ThatDogKofu"), 12),  # Saturday AM
            (start_date + timedelta(days=1), ("sledgelp", "ikodomoonstrife"), 12),  # Saturday PM
            (start_date + timedelta(days=1.5), ("silvixen", "kaideart"), 12),  # Sunday AM
            (start_date + timedelta(days=2), ("LeonFoxy", "Nanukk"), 12),  # Sunday PM
            (start_date + timedelta(days=2.5), ("ThrVirtualFloof", "BlueBirdBreeze"), 12),  # Monday AM
            (start_date + timedelta(days=3), ("vrcvictory", "Wulf97"), 12),  # Monday PM
            (start_date + timedelta(days=3.5), ("Wishdream", "BlueBoxey"), 12),  # Tuesday AM
            (start_date + timedelta(days=4), ("SnoweyVR", "Heartwood"), 12),  # Tuesday PM
            (start_date + timedelta(days=4.5), ("sammifawkes", "undertheredmoon"), 12),  # Wednesday AM
            (start_date + timedelta(days=5), ("neon_woof", "electrowuff"), 12),  # Wednesday PM
            (start_date + timedelta(days=5.5), ("megaacat", "merlekoz"), 12),  # Thursday AM
            (start_date + timedelta(days=6), ("dutchwolffe", "anubian_nomad"), 12),  # Thursday PM
            (start_date + timedelta(days=6.5), ("DannoGSD", "CorgiCraft"), 12),  # Friday AM
            (start_date + timedelta(days=7), ("aydanfox", "luiroilefuret"), 12),  # Friday PM
            (start_date + timedelta(days=7.5), ("BardicRJ", "ItsMapleDoe"), 12),  # Saturday AM (FINALE)
        ]
    current_streamers = None
    current_charity = None
    for startdate, streamer_pair, slot_hours in timeslots:
        if startdate < now() < startdate+timedelta(hours=slot_hours):
            current_streamers = streamer_pair
            break
    for charity in charity_list:
        if charity.slot < now() < charity.slot+timedelta(days=1):
            current_charity = charity
            break
    grand_total = lifetime_data['grand_total']
    return render_template("index.html", charities=charity_list, timeslots=timeslots, now=now(), timedelta=timedelta,
                           current_streamer=current_streamers, current_charity=current_charity, grand_total=grand_total)


@app.route("/update", methods=["POST"])
def update():
    data = request.get_json()
    lifetime_data['grand_total'] = data['total']['value']
    for campaign_id, campaign_data in data['charity_data'].items():
        for charity in charity_list:
            if charity.wilddogs_campaign.id == campaign_id:
                charity.wilddogs_campaign.total_raised = float(campaign_data['value'])
                break
            if charity.antlers_campaign.id == campaign_id:
                charity.antlers_campaign.total_raised = float(campaign_data['value'])
                break
            if charity.outlanders_campaign.id == campaign_id:
                charity.outlanders_campaign.total_raised = float(campaign_data['value'])
                break
    return Response(status=204)
    pass


async def refresh_tiltify_token():

    pass

#
# @app.route("/data/total_raised")
# async def total_raised():
#     response = dict(
#         grand_total=dict(currency="USD", value="0.00"),
#         wilddogs=dict(currency="USD", value="0.00"),
#         antlers=dict(currency="USD", value="0.00"),
#         outlanders=dict(currency="USD", value="0.00")
#     )
#     return Response(json.dumps(response), status=200, mimetype="application/json")


app.config["FREEZER_RELATIVE_URLS"] = True

freezer = Freezer(app)

# celery_app = celery_init_app(app)

if __name__ == "__main__":
    # freezer.freeze()
    app.run(threaded=True) #, debug=True)
