import os
import requests
from dotenv import load_dotenv

load_dotenv()
# Using Proxy curl to request to streamline Linkedin api call
# https://nubela.co/proxycurl/dashboard/proxycurl-api/
# Using a gist to enable making an api call but not use all 10 new user tokens awarded from proxycurl - made one call then stored JSON data at the following public gist link
# https://gist.githubusercontent.com/jinman36/2e6195537e362197ade2f6804dbf3184/raw/3606249159b0d79903afa882949367e8c817349d/ji_test.json

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information from LinkedIN profiles, manually scrape the informaiton from the LinkedIn profile"""
    
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/jinman36/2e6195537e362197ade2f6804dbf3184/raw/3606249159b0d79903afa882949367e8c817349d/ji_test.json"
        response = requests.get(
            linkedin_profile_url,
            timeout=10
        )
    else:
        header_dic = {'Authorization': f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=header_dic,
            timeout=10
        )  

    data = response.json()
    
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")
    
    
    return data


if __name__ == "__main__":
    print(scrape_linkedin_profile(linkedin_profile_url = "https://gist.githubusercontent.com/jinman36/2e6195537e362197ade2f6804dbf3184/raw/3606249159b0d79903afa882949367e8c817349d/ji_test.json", mock=True))
