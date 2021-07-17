#!/usr/bin/env python
import toml

print(toml.__file__)

test_str = """
        # Global tags can be specified here in key="value" format.
        [global_tags]
        # dc = "us-east-1" # will tag all metrics with dc=us-east-1
        # rack = "1a"
        ## Environment variables can be used as tags, and throughout the config file
        # user = "$USER"


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

decoder.remove_before_duplicates()


print("______________________________________")
from pprint import pprint
pprint(decoder.before_tags)
print("______________________________________")


# Global tags
assert decoder.before_tags["global_tags"] == {
    "comments": ["""Global tags can be specified here in key="value" format."""],
    "children" : [],
}

# Agent
assert decoder.before_tags["agent"] == {
    "comments" : ["""Configuration for telegraf agent"""],
    "children" : [
        {
            "name" : "interval",
            "comments": [
                "Default data collection interval for all inputs"
            ]
        }, {
            "name" : "round_interval",
            "comments" : [
                "Rounds collection interval to 'interval'",
                """ie, if interval="10s" then always collect on :00, :10, :20, etc.""",
            ]
        }
    ]
}

assert decoder.before_tags["inputs.azure_storage_queue"] == {
    "comments" : "Gather Azure Storage Queue metrics",
    "children" : [
        {
            "name" : "account_name",
            "comments" : [
                "Required Azure Storage Account name",
                "Inline comment"
            ]
        }, {
            "name": "account_key",
            "comments" :[
                "Required Azure Storage Account access key",

            ]
        },{
            "name" : "peek_oldest_message_age",
            "comments" :[
                """Set to false to disable peeking age of oldest message (executes faster)"""
            ]
        }
    ]
}



print(data)