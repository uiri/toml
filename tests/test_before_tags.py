#!/usr/bin/env python
import toml




def test_before_comments():
    """Tests handling before comments"""
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

def test_bugfix_incorrect_comments():
    """
    Tests bug that causes comments to be put with the wrong item
    """
    test_str = """
        [[inputs.vsphere]]
        #   ## List of vCenter URLs to be monitored. These three lines must be uncommented
        #   ## and edited for the plugin to work.

        vcenters = [ "https://vcenter.local/sdk" ]
        username = "user@corp.local"
        password = "secret"

        #   ## VMs
        #   ## Typical VM metrics (if omitted or empty, all metrics are collected)
        vm_include = [ "/*/vm/**"] # Inventory path to VMs to collect (by default all are collected)
        vm_exclude = [] # Inventory paths to exclude
        vm_metric_include = ["cpu.demand.average","cpu.idle.summation",]
        vm_metric_exclude = [] ## Nothing is excluded by default
        vm_instances = true ## true by default

        #   ## Hosts

        #   ## Typical host metrics (if omitted or empty, all metrics are collected)

        host_include = [ "/*/host/**"] # Inventory path to hosts to collect (by default all are collected)
        #   # host_exclude [] # Inventory paths to exclude

        host_metric_include = ["cpu.coreUtilization.average","cpu.costop.summation",]
        #   ## Clusters

        cluster_include = [ "/*/host/**"] # Inventory path to clusters to collect (by default all are collected)
        cluster_exclude = [] # Inventory paths to exclude
        cluster_metric_include = [] ## if omitted or empty, all metrics are collected
        cluster_metric_exclude = [] ## Nothing excluded by default
        cluster_instances = false ## false by default

        #   ## Datastores

        datastore_include = [ "/*/datastore/**"] # Inventory path to datastores to collect (by default all are collected)
        datastore_exclude = [] # Inventory paths to exclude
        datastore_metric_include = [] ## if omitted or empty, all metrics are collected
        datastore_metric_exclude = [] ## Nothing excluded by default
        datastore_instances = false ## false by default

        #   ## Datacenters

        datacenter_include = [ "/*/host/**"] # Inventory path to clusters to collect (by default all are collected)
        datacenter_exclude = [] # Inventory paths to exclude
        datacenter_metric_include = [] ## if omitted or empty, all metrics are collected
        datacenter_metric_exclude = [ "*" ] ## Datacenters are not collected by default.
        datacenter_instances = false ## false by default

        #   ## Plugin Settings
        #   ## separator character to use for measurement and field names (default: "_")

        separator = "_"

        #   ## number of objects to retrieve per query for realtime resources (vms and hosts)
        #   ## set to 64 for vCenter 5.5 and 6.0 (default: 256)

        max_query_objects = 256

        #   ## number of metrics to retrieve per query for non-realtime resources (clusters and datastores)
        #   ## set to 64 for vCenter 5.5 and 6.0 (default: 256)

        max_query_metrics = 256

        #   ## number of go routines to use for collection and discovery of objects and metrics

        collect_concurrency = 1
        discover_concurrency = 1

        #   ## the interval before (re)discovering objects subject to metrics collection (default: 300s)

        object_discovery_interval = "300s"

        #   ## timeout applies to any of the api request made to vcenter

        timeout = "60s"

        #   ## When set to true, all samples are sent as integers. This makes the output
        #   ## data types backwards compatible with Telegraf 1.9 or lower. Normally all
        #   ## samples from vCenter, with the exception of percentages, are integer
        #   ## values, but under some conditions, some averaging takes place internally in
        #   ## the plugin. Setting this flag to "false" will send values as floats to
        #   ## preserve the full precision when averaging takes place.

        use_int_samples = true

        #   ## Custom attributes from vCenter can be very useful for queries in order to slice the
        #   ## metrics along different dimension and for forming ad-hoc relationships. They are disabled
        #   ## by default, since they can add a considerable amount of tags to the resulting metrics. To
        #   ## enable, simply set custom_attribute_exclude to [] (empty set) and use custom_attribute_include
        #   ## to select the attributes you want to include.
        #   ## By default, since they can add a considerable amount of tags to the resulting metrics. To
        #   ## enable, simply set custom_attribute_exclude to [] (empty set) and use custom_attribute_include
        #   ## to select the attributes you want to include.

        custom_attribute_include = []
        custom_attribute_exclude = ["*"]

        #   ## The number of vSphere 5 minute metric collection cycles to look back for non-realtime metrics. In
        #   ## some versions (6.7, 7.0 and possible more), certain metrics, such as cluster metrics, may be reported
        #   ## with a significant delay (>30min). If this happens, try increasing this number. Please note that increasing
        #   ## it too much may cause performance issues.

        metric_lookback = 3

        #   ## Optional SSL Config

        ssl_ca = "/path/to/cafile"
        ssl_cert = "/path/to/certfile"
        ssl_key = "/path/to/keyfile"
        #   ## Use SSL but skip chain & host verification

        insecure_skip_verify = false

        #   ## The Historical Interval value must match EXACTLY the interval in the daily
        #   # "Interval Duration" found on the VCenter server under Configure > General > Statistics > Statistic intervals

        historical_interval = "5m"


        # # A Webhooks Event collector

        [[inputs.webhooks]]
        #   ## Address and port to host Webhook listener on
        service_address = ":1619"
    """
    decoder = toml.TomlPreserveCommentDecoder(beforeComments=True)
    data = toml.loads(test_str, decoder=decoder)

    assert "Address and port to host Webhook listener on" in decoder.before_tags[-1]["comments"] 

    assert "Nothing is excluded by default" in decoder.before_tags[7]["comments"]