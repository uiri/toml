#!/usr/bin/env python
import toml

TEST_STR = """
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


def test_before_comments():
    """Tests handling before comments"""

    decoder = toml.TomlPreserveCommentDecoder(beforeComments=True)
    data = toml.loads(TEST_STR, decoder=decoder)

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
        "comments": [
            """dc = "us-east-1" # will tag all metrics with dc=us-east-1""",
            'rack = "1a"',
            """Environment variables can be used as tags, and throughout the config file"""
        ],
        "parent": "[global_tags]"
    }

    assert parsed_tags["user = \"$USER\""] == expected

    # Agent
    expected = {
        "comments": ["""Configuration for telegraf agent"""],
    }

    assert parsed_tags["[agent]"] == expected

    # interval = "10s"
    expected = {
        "comments": [
            "Default data collection interval for all inputs"
        ],
        "parent": "[agent]"
    }
    assert parsed_tags["interval = \"10s\""] == expected

    # round_interval = true
    expected = {
        "comments": [
            "Rounds collection interval to 'interval'",
            'ie, if interval="10s" then always collect on :00, :10, :20, etc.'
        ],
        "parent": "[agent]"
    }
    assert parsed_tags["round_interval = true"] == expected

    expected = {
        "comments": ["Gather Azure Storage Queue metrics"]
    }

    assert parsed_tags["[[inputs.azure_storage_queue]]"] == expected

    # account_name

    expected = {
        "comments": [
            "Required Azure Storage Account name",
            "Inline comment"
        ],
        "parent": "[[inputs.azure_storage_queue]]"
    }

    assert parsed_tags["account_name = \"mystorageaccount\""] == expected

    # account_key
    expected = {
        "comments": [
            "Required Azure Storage Account access key"
        ],
        "parent": "[[inputs.azure_storage_queue]]"
    }

    assert parsed_tags["account_key = \"storageaccountaccesskey\""] == expected

    # peek_oldest_message_age

    expected = {
        "comments": [
            "Set to false to disable peeking age of oldest message (executes faster)"
        ],
        "parent": "[[inputs.azure_storage_queue]]"
    }

    assert parsed_tags["peek_oldest_message_age = true"] == expected

def test_bugfix_improper_parents():
    """
    Tests bug that sets arrays to be parents due to [ ] being present
    """
    test_str = """
    [[outputs.influxdb]]   
    ## The full HTTP or UDP URL for your InfluxDB instance.   
    ##  
    ## Multiple URLs can be specified for a single cluster, only ONE of the  
    ## urls will be written to each interval.   
    # urls = ["unix:///var/run/influxdb.sock"]  
    # urls = ["udp://127.0.0.1:8089"]   
    urls = ["http://127.0.0.1:8086"]   

    ## The target database for metrics; will be created as needed.   
    ## For UDP url endpoint database needs to be configured on server side.   
    # database = "telegraf"   
    ## The value of this tag will be used to determine the database.  If this   
    ## tag is not set the 'database' option is used as the default.   
    database_tag = ""
    """

    decoder = toml.TomlPreserveCommentDecoder(beforeComments=True)
    data = toml.loads(test_str, decoder=decoder)

    assert decoder.before_tags[-1]["parent"] == "[[outputs.influxdb]]"