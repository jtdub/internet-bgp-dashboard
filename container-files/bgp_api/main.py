#!/usr/bin/env python3

import requests
import logging
from time import time
from fastapi import FastAPI


cache = {"expires_at": time(), "data": None} 
app = FastAPI()

logging.basicConfig(
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.DEBUG
)


def get_data(url: str, expire: int=600) -> dict:
    """Fetch data from API if the data doesn't exist and the data hasn't expired.
    Otherwise, fetch data from cache.

    Args:
        url (str): URL to fetch data from
        expire (int): cache expiration in seconds

    Returns:
        cache['data'] (dict): Results of data
    """
    if cache["data"] is None:
        write_cache(data=get_data_from_server(url=url), expire=expire)
        return cache["data"]

    if cache["expires_at"] >= time():
        logging.info("cache hasn't expired. fetching data from cache")
        return cache["data"]

    write_cache(data=get_data_from_server(url=url), expire=expire)
    return cache["data"]


def get_data_from_server(url: str) -> dict:
    """Fetch data from server

    Args:
        url (str): URL to fetch data from

    Returns:
        resp.json() (dict): Results from request
    """
    logging.info(f"fetching {url} data from server")
    headers = {"Accept": "application/json", "Content-type": "application/json"}
    resp = requests.get(url=url, headers=headers)

    if resp.ok:
        logging.info(f"{url} response is {resp.status_code}")
        return resp.json()
    return resp.raise_for_status()


def write_cache(data: dict, expire: int=600) -> dict:
    """Write data to in memory cache

    Args:
        data (dict): data to write to cache
        expire (int): expiration of cache in seconds

    Returns:
        data (dict): data written to cache
    """
    cache["expires_at"] = time() + expire
    cache["data"] = data 
    logging.info(f"data expires at {cache['expires_at']}")
    logging.info(f"data written to cache: {cache['data']}")
    return data


@app.get("/")
def home():
    return get_data("https://bgpstuff.net/totals")
