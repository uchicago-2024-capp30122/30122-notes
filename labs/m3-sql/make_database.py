"""
This script takes Congressional data from

https://raw.githubusercontent.com/unitedstates/congress-legislators/main/legislators-current.yaml

and creates a database of legislators.

You do not need to run this script, it has already been run and the
 database is included in the repository.

It may be helpful to look at this script to see examples of how to
use the sqlite3 module to create and populate a database.
"""

import yaml
import sqlite3
import requests


def create_tables():
    """
    Create the tables in the database.
    """
    db = sqlite3.connect("legislators.db")
    db.execute(
        """CREATE TABLE legislators (
        bioguide_id VARCHAR PRIMARY KEY,
        first_name VARCHAR NOT NULL,
        last_name VARCHAR NOT NULL,
        birthday DATE NOT NULL,
        gender VARCHAR NOT NULL,
        current_chamber VARCHAR NOT NULL,
        current_state VARCHAR NOT NULL,
        current_district INTEGER,
        current_party VARCHAR NOT NULL
        )
        """
    )
    db.execute(
        """
        CREATE TABLE roles (
        bioguide_id VARCHAR NOT NULL,
        chamber VARCHAR NOT NULL,
        state VARCHAR NOT NULL,
        district INTEGER,
        party VARCHAR NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE,
        FOREIGN KEY (bioguide_id) REFERENCES legislators (bioguide_id)
        )
        """
    )
    db.execute(
        """
        CREATE TABLE other_identifiers (
            bioguide_id VARCHAR NOT NULL,
            type VARCHAR NOT NULL,
            value VARCHAR NOT NULL,
            FOREIGN KEY (bioguide_id) REFERENCES legislators (bioguide_id)
        )"""
    )


def get_legislators():
    """
    Return a list of legislators.
    """
    url = "https://raw.githubusercontent.com/unitedstates/congress-legislators/main/legislators-current.yaml"
    return yaml.safe_load(requests.get(url).text)


def load_legislators(legislators):
    """
    Load the legislators into the database.
    """
    db = sqlite3.connect("legislators.db")
    for legislator in legislators:
        db.execute(
            """
            INSERT INTO legislators
             (bioguide_id, first_name, last_name, birthday, gender, current_chamber, current_state, current_district, current_party)
            VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
            (
                legislator["id"]["bioguide"],
                legislator["name"]["first"],
                legislator["name"]["last"],
                legislator["bio"]["birthday"],
                legislator["bio"]["gender"],
                legislator["terms"][-1]["type"],
                legislator["terms"][-1]["state"],
                legislator["terms"][-1].get("district", None),
                legislator["terms"][-1]["party"],
            ),
        )
        for role in legislator["terms"]:
            db.execute(
                """
                INSERT INTO roles
                    (bioguide_id, chamber, state, district, party, start_date, end_date)
                VALUES
                    (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    legislator["id"]["bioguide"],
                    role["type"],
                    role["state"],
                    role.get("district", None),
                    role["party"],
                    role["start"],
                    role["end"],
                ),
            )
        for identifier, values in legislator["id"].items():
            # coerce to list, some ids are multivalued
            if not isinstance(values, list):
                values = [values]
            for value in values:
                db.execute(
                    """
                    INSERT INTO other_identifiers
                        (bioguide_id, type, value)
                    VALUES
                        (?, ?, ?)
                    """,
                    (
                        legislator["id"]["bioguide"],
                        identifier,
                        value,
                    ),
                )
    db.commit()


def main():
    legislators = get_legislators()
    create_tables()
    load_legislators(legislators)


if __name__ == "__main__":
    main()
