#!/usr/bin/env python
import toml
from pprint import pprint

def test_before_comments():
    """Tests handling before comments"""
    test_str = """
            # Global tags can be specified here in key="value" format.
            [global_tags]
            # dc = "us-east-1" # will tag all metrics with dc=us-east-1
            # rack = "1a"
            ## Environment variables can be used as tags, and throughout the config file
            user = "$USER"


            # Configuration for telegraf agent
            [agent]
            ## Default data collection interval for all inputs
            interval = "10s"
            ## Rounds collection interval to 'interval'
            ## ie, if interval="10s" then always collect on :00, :10, :20, etc.
            round_interval = true

            # # Gather Azure Storage Queue metrics
            [[inputs.azure_storage_queue]]

            #   ## Required Azure Storage Account name

                account_name = "mystorageaccount" # Inline comment
            #
            #   ## Required Azure Storage Account access key
                account_key = "storageaccountaccesskey"
            #
            #   ## Set to false to disable peeking age of oldest message (executes faster)
                peek_oldest_message_age = true
    """
    decoder = toml.TomlPreserveCommentDecoder(beforeComments=True)
    data = toml.loads(test_str, decoder=decoder)

    parsed_tags = {}
    
    for line in decoder.before_tags:
        parsed_tags[line["name"]] = line
        del parsed_tags[line["name"]]["name"]


    # Global tags
    assert parsed_tags["[global_tags]"] == {
        "comments": ["""Global tags can be specified here in key="value" format."""],
    }

    # user = "$USER"
    expected = {
        "comments" : [
            """dc = "us-east-1" # will tag all metrics with dc=us-east-1""",
            'rack = "1a"',
            """Environment variables can be used as tags, and throughout the config file"""
        ],
        "parent" : "[global_tags]"
    }
    

    assert parsed_tags["user = \"$USER\""] == expected

    # Agent
    expected = {
        "comments" : ["""Configuration for telegraf agent"""],
    }
    
    assert parsed_tags["[agent]"] == expected

    # interval = "10s"
    expected = {
        "comments": [
            "Default data collection interval for all inputs"
        ],
        "parent" : "[agent]"
    }
    assert parsed_tags["interval = \"10s\""] == expected

    # round_interval = true
    expected = {
        "comments" : [
            "Rounds collection interval to 'interval'",
            'ie, if interval="10s" then always collect on :00, :10, :20, etc.'
        ],
        "parent" : "[agent]"
    }
    assert parsed_tags["round_interval = true"] == expected



    expected = {
        "comments" : ["Gather Azure Storage Queue metrics"]
    }

    assert parsed_tags["[[inputs.azure_storage_queue]]"] == expected

    # account_name

    expected = {
        "comments" : [
            ""
        ]
    }
    assert parsed_tags["account_name = \"mystorageaccount\""] == expected

    # account_key
    expected = {}
    assert parsed_tags["account_key = \"storageaccountaccesskey\""] == expected

    # peek_oldest_message_age

    expected = {}
    assert parsed_tags["peak_oldest_message_age = true"] == expected

if __name__ == "__main__":
    test_before_comments()