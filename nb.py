import requests
import urllib.parse

import pandas as pd


class NB_Base:
    def __init__(self, slug, token, default_site=None):
        self.NATION_SLUG = slug
        self.API_KEY = token
        self.URL_CAP = f"limit=1000&access_token={self.API_KEY}"
        self.NEXT_URL = "".join(
            ["https://", self.NATION_SLUG, ".nationbuilder.com"]
        )
        self.BASE_URL = "".join([self.NEXT_URL, "/api/v1"])
        self.site_loaded = default_site
        self.site_dict = {}
        self._safe_mode_status = True

        # * Simple Endpoint URLS
        self.CAMPAIGN_DATE_URL = self.BASE_URL + "/campaign_data"
        self.CONTACT_TYPES_URL = self.BASE_URL + "/settings/contact_types"
        self.DONATIONS_URL = self.BASE_URL + "/donations"
        self.IMPORTS_URL = self.BASE_URL + "/imports"
        self.EXPORTS_URL = self.BASE_URL + "/exports"
        self.LISTS_URL = self.BASE_URL + "/lists"
        self.PATHS_URL = self.BASE_URL + "/paths"
        self.PEOPLE_URL = self.BASE_URL + "/people"
        self.TAGS_URL = self.BASE_URL + "/tags"
        self.PRECINCTS_URL = self.BASE_URL + "/precincts"
        self.SURVEY_RESPONSES_URL = self.BASE_URL + "/survey_responses"

        self.SITES_URL = self.BASE_URL + "/sites"
        self.PAGE_TYPE_URL = self.SITES_URL + "/" + self.site_loaded + "/pages"
        self.BASIC_PAGES_URL = self.PAGE_TYPE_URL + "/basic_pages"
        self.BLOG_POST_URL = self.PAGE_TYPE_URL + "/blogs"
        self.CALENDARS_URL = self.PAGE_TYPE_URL + "/calendars"
        self.EVENTS_URL = self.PAGE_TYPE_URL + "/events"
        self.PETITIONS_URL = self.PAGE_TYPE_URL + "/petitions"
        self.SURVEYS_URL = self.PAGE_TYPE_URL + "/surveys"

    # * Decorators
    # TODO I'd like to not have to add these to every function I'd like to call,
    # TODO maybe the safe_mode one is okay though hhhh

    def check_safe_mode(func):
        def wrapper(self, *args, **kwargs):
            if self._safe_mode_status is True:
                print(
                    f"'{func.__name__}' has been blocked because program is in Safe Mode Active"
                )
            else:
                return func(self, *args, **kwargs)

        return wrapper

    @check_safe_mode
    def test_s(self):
        return print("test func ran")

    def test_c(self):
        return f"{__class__}"

    def safe_mode(self, flag=True):
        self._safe_mode_status = flag
        if self._safe_mode_status is False:
            print("Safe Mode has been Deactivated")
        else:
            print("Safe Mode has been Activated")

    # * Common functionality

    def pagination(self, token='', nonce='') -> str:
        limit = str(limit) if limit != '' else ''
        api_parm = [
            (token, "__token="),
            (nonce, "__nonce=")
        ]
        api_parm = [
            api_parm[i][1] + api_parm[i][0]
            for i in range(0, len(api_parm))
            if api_parm[i][0] != ''
        ]
        api_parm = f"{"&".join(api_parm)}&{self.URL_CAP}"
        return api_parm

    def next_page(self, resp):
        return requests.get(
            self.NEXT_URL +
            resp.json()["next"] +
            f"&{self.URL_CAP}"
        )

    def pull_status(self, resp):
        print(
            "  ".join(
                [
                    f"{resp.headers["Date"]}",
                    f"Status Code: {resp.status_code}",
                    f"Rate Limit: {
                        resp.headers["nation-ratelimit-remaining"]}"
                ]
            )
        )

    def all_results(self, resp, datatype="df"):
        results = resp.json()["results"]
        results_df = pd.DataFrame(results)
        if resp.json()["next"] is not None:
            while True:
                resp = self.next_page(resp)
                resp_df = pd.DataFrame(resp.json()["results"])
                self.pull_status(resp)
                results_df = pd.concat(
                    [results_df, resp_df], ignore_index=True)
                if resp.json()["next"] is None:
                    break
        if datatype == "df":
            return results_df
        else:
            return results_df

    def index_sites(self, return_resp=True):
        resp = requests.get(
            f"{self.SITES_URL}?{self.URL_CAP}"
        )
        if resp.status_code == 200:
            for i in resp.json()["results"]:
                self.site_dict[i["name"]] = i
            print("Sites Request Successful, Sites Loaded")
        else:
            print("Sites Request Fail")
        if return_resp:
            return resp


class Contact_Types(NB_Base):
    def __init__(self, slug, token, default_site):
        super().__init__(slug, token, default_site)

    def test_c(self):
        return f"{__class__}"


class Donations(NB_Base):
    def __init__(self, slug, token, default_site):
        super().__init__(slug, token, default_site)

    def test_c(self):
        return f"{__class__}"


class Imports(NB_Base):
    def __init__(self, slug, token, default_site):
        super().__init__(slug, token, default_site)

    def test_c(self):
        return f"{__class__}"


class Exports(NB_Base):
    def __init__(self, slug, token, default_site):
        super().__init__(slug, token, default_site)

    def test_c(self):
        return f"{__class__}"


class NB_Lists(NB_Base):
    def __init__(self, slug, token, default_site):
        super().__init__(slug, token, default_site)

    def test_c(self):
        return f"{__class__}"

    def index(self):
        resp = requests.get(
            f"{self.LISTS_URL}?{self.URL_CAP}"
        )
        return resp

    def people(self, person_id):
        resp = requests.get(
            f"{self.LISTS_URL}/{person_id}/people?{self.URL_CAP}"
        )
        return resp
    
    def add_people(self, person_id):
        resp = requests.post(
            f"{self.LISTS_URL}/{person_id}/people?{self.URL_CAP}"
        )

class Memberships(NB_Base):
    def __init__(self, slug, token, default_site):
        super().__init__(slug, token, default_site)

    def test_c(self):
        return f"{__class__}"
    
    def index(self, person_id):
        resp = requests.get(
            f"{self.PEOPLE_URL}/{person_id}/memberships?{self.URL_CAP}"
        )
        return resp

class People(NB_Base):
    """
    Used to get at the People API

    See http://nationbuilder.com/people_api for info on the data returned
    """

    def __init__(self, slug, token, default_site):
        super().__init__(slug, token, default_site)

    def test_c(self):
        return f"{__class__}"

    def index(self):
        resp = requests.get(
            f"{self.PEOPLE_URL}?{self.URL_CAP}"
        )
        return resp

    def count(self):
        resp = requests.get(
            f"{self.PEOPLE_URL}/count?{self.URL_CAP}"
        )
        return resp

    def show(self, person_id):
        resp = requests.get(
            f"{self.PEOPLE_URL}/show?{self.URL_CAP}"
        )
        return resp

    def match(self, email):
        resp = requests.get(
            f"{self.PEOPLE_URL}/match?{self.URL_CAP}",
            params={
                "email": email
            }
        )
        return resp

    def me(self):
        resp = requests.get(
            f"{self.PEOPLE_URL}/me?{self.URL_CAP}"
        )
        return resp

    def update(self, nb_id, nb_data):
        # x = f"{self.PEOPLE_URL}/{nb_id}?access_token={self.API_KEY}",
        # y = data = nb_data

        resp = requests.put(
            f"{self.PEOPLE_URL}/{nb_id}?{self.URL_CAP}",
            json=nb_data
        )
        return resp

    def tag_person(self, nb_id, nb_tag):
        resp = requests.put(
            f"{self.PEOPLE_URL}/{nb_id}/taggings?{self.URL_CAP}",
            json={
                "tagging": {
                    "tag": nb_tag
                }
            }
        )
        return resp

    def tag_removal(self, nb_id, nb_tag):
        nb_tag = urllib.parse.quote(nb_tag, safe='')
        resp = requests.delete(
            f"{self.PEOPLE_URL}/{nb_id}/taggings/{nb_tag}?{self.URL_CAP}"
        )
        return resp

    # def show(self, person_id):
    #     """
    #     Retrieves a person's record from NationBuilder.

    #     Parameters:
    #         person_id - The person's NationBuilder ID.

    #     Returns:
    #         A person record, as a dict.
    #     """
    #     # we need it as a string...
    #     person_id = str(person_id)
    #     url = self.PEOPLE_URL.format(person_id)
    #     headers, content = self.http.request(url, headers=self.HEADERS)
    #     self._check_response(headers, content, "Get Person", url)
    #     return json.loads(content)

    # def x(self):
    #     self.PEOPLE_URL.format(person_id)
    #     pass

    # def me(self):
    #     """Fetches the Access token owner's profile"""
    #     # self._authorise()
    #     url = self.PEOPLE_URL + "/me"
    #     hdr, cnt = self.http.request(uri=url, headers=self.HEADERS)
    #     self._check_response(hdr, cnt, "Get Me", url)
    #     return json.loads(cnt)


class NB_Tags(People):
    def __init__(self, slug, token, default_site):
        super().__init__(slug, token, default_site)

    def test_c(self):
        return f"{__class__}"

    def index(self):
        resp = requests.get(
            f"{self.TAGS_URL}?{self.URL_CAP}"
        )
        return resp

    def people(self, tag):
        tag = urllib.parse.quote(tag, safe='')
        resp = requests.get(
            f"{self.TAGS_URL}/{tag}/people?{self.URL_CAP}"
        )
        return resp


class Sites(NB_Base):
    def __init__(self, slug, token, default_site):
        super().__init__(slug, token, default_site)

    def test_c(self):
        return f"{__class__}"


class BasicPages(Sites):
    def __init__(self, slug, token, default_site):
        super().__init__(slug, token, default_site)

    def test_c(self):
        return f"{__class__}"


class Blogs(Sites):
    def __init__(self, slug, token, default_site):
        super().__init__(slug, token, default_site)

    def test_c(self):
        return f"{__class__}"


class Blogs_Posts(Sites):
    def __init__(self, slug, token, default_site):
        super().__init__(slug, token, default_site)

    def test_c(self):
        return f"{__class__}"


class Calendars(Sites):
    def __init__(self, slug, token, default_site):
        super().__init__(slug, token, default_site)

    def test_c(self):
        return f"{__class__}"


class Events(Sites):
    def __init__(self, slug, token, default_site):
        super().__init__(slug, token, default_site)

    def test_c(self):
        return f"{__class__}"

    def index(
            self, site_slug="2019", tags=None,
            starting=None, until=None, calendar_id=None):

        resp = requests.get(
            f"{self.EVENTS_URL}?{self.URL_CAP}",
            params={
                "tags": tags,
                "starting": starting,
                "until": until,
                "calendar_id": calendar_id
            }
        )
        return resp

    def events_create(self, nb_data, site_slug="2019"):
        resp = requests.post(
            f"{self.EVENTS_URL}?{self.URL_CAP}",
            json=nb_data
        )
        return resp

    def event_destroy(self, event_id, site_slug="2019"):
        resp = requests.delete(
            f"{self.EVENTS_URL}/{event_id}?{self.URL_CAP}"
        )
        return resp

    def rsvps(self, event_id, site_slug="2019"):
        resp = requests.get(
            f"{self.EVENTS_URL}/{event_id}/rsvps?{self.URL_CAP}",
        )
        return resp

    def rsvp_create(self, event_id, nb_data, site_slug="2019"):
        resp = requests.post(
            f"{self.EVENTS_URL}/{event_id}/rsvps?{self.URL_CAP}",
            json=nb_data
        )
        return resp.json()


class Petitions(Sites):
    def __init__(self, slug, token, default_site):
        super().__init__(slug, token, default_site)

    def test_c(self):
        return f"{__class__}"


class Surveys(Sites):
    def __init__(self, slug, token, default_site):
        super().__init__(slug, token, default_site)

    def test_c(self):
        return f"{__class__}"


class N_Bee(NB_Base):
    """
    Entry point to nationbuilder APIs.

    Public attributes:
        people : nbpy.people.People instance for accessing people API
        tags : nbpy.tags.NBTags instance for accessing People Tags API
        lists : nbpy.lists.NBList instance for accessing Lists API
    """

    def __init__(self, slug, token, default_site=''):
        super().__init__(slug, token, default_site)

        self.people = People(self.NATION_SLUG, self.API_KEY, self.site_loaded)
        self.tags = NB_Tags(self.NATION_SLUG, self.API_KEY, self.site_loaded)
        self.events = Events(self.NATION_SLUG, self.API_KEY, self.site_loaded)
        self.lists = NB_Lists(self.NATION_SLUG, self.API_KEY, self.site_loaded)
        self.memberships = Memberships(self.NATION_SLUG, self.API_KEY, self.site_loaded)
        # self.contacts = Contacts(
        # self.NATION_SLUG, self.API_KEY, self.site_loaded
        # )
        self.index_sites(return_resp=False)

    def test_c(self):
        return f"{__class__}"

    # * General Site methods

    def man(self, parms='', req="get"):
        if req == "get":
            resp = requests.get("https://" + parms)
            return resp
        # elif requests.post

    # TODO This should probably be moved

    def set_site(self, site, from_site_dict=True):
        if self.site_dict == None:
            self.index_sites()
        if from_site_dict:
            self.site_loaded = self.site_dict[site]

    def campaign_data(self):
        resp = requests.get(
            f"{self.CAMPAIGN_DATE_URL}?{self.URL_CAP}"
        )
        return resp

    def paths(self):
        resp = requests.get(
            f"{self.PATHS_URL}?{self.URL_CAP}"
        )
        return resp

    def paths(self):
        resp = requests.get(
            f"{self.PEOPLE_URL}?{self.URL_CAP}"
        )
        return resp


def from_file(f):
    """
    Factory method that creates a NationBuilder instance from a file containing
    the nation slug and the api key.

    The format of the file is as follows:

        slug: slug
        api_key: key

    pretty simple I reckon.
    """
    with open(f, "r") as creds:
        slug = None
        key = None
        site = None
        for line in creds:
            parts = line.split(":")
            if parts[0].strip() == "slug":
                slug = parts[1].strip()
            elif parts[0].strip() == "api_key":
                key = parts[1].strip()
            elif parts[0].strip() == "default_site":
                site = str(parts[1].strip())
        if slug is not None and key is not None and site is not None:
            return N_Bee(slug, key, site)
        elif slug is not None and key is not None:
            return N_Bee(slug, key)
        return None
