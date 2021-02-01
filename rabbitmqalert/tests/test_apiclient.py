#! /usr/bin/python2
# -*- coding: utf8 -*-

import json
import mock
import unittest
import urllib2

from rabbitmqalert import apiclient


class ApiClientTestCase(unittest.TestCase):

    def setUp(self):
        apiclient.json_real = apiclient.json
        apiclient.urllib2_real = apiclient.urllib2

    def tearDown(self):
        apiclient.json = apiclient.json_real
        apiclient.urllib2 = apiclient.urllib2_real

    def test_get_queue_returns_result_when_no_error(self):
        logger = mock.MagicMock()
        arguments = self.construct_arguments()

        client = apiclient.ApiClient(logger, arguments)
        client.send_request = mock.MagicMock(return_value=self.construct_response_queue())
        response = client.get_queue()

        uri = "/api/queues/%s/%s" % (arguments["server_vhost"], arguments["server_queue"])
        client.send_request.assert_called_once_with(uri)
        self.assertEquals(self.construct_response_queue(), response)

    def test_get_queue_returns_none_when_error(self):
        logger = mock.MagicMock()
        arguments = self.construct_arguments()

        client = apiclient.ApiClient(logger, arguments)
        client.send_request = mock.MagicMock(return_value=None)
        apiclient.urllib2.build_opener.open = mock.MagicMock(side_effect=urllib2.HTTPError)
        response = client.get_queue()

        uri = "/api/queues/%s/%s" % (arguments["server_vhost"], arguments["server_queue"])
        client.send_request.assert_called_once_with(uri)
        self.assertEquals(None, response)

    def test_get_queues_returns_queues_when_exist(self):
        logger = mock.MagicMock()
        arguments = self.construct_arguments()

        client = apiclient.ApiClient(logger, arguments)
        client.send_request = mock.MagicMock(return_value=self.construct_response_queues())
        queues = client.get_queues()

        logger.info.assert_called_once()
        logger.error.assert_not_called()
        client.send_request.assert_called_once()
        self.assertEquals(["foo", "bar"], queues)

    def test_get_queues_returns_empty_list_when_no_queues_exist(self):
        logger = mock.MagicMock()
        arguments = self.construct_arguments()

        client = apiclient.ApiClient(logger, arguments)
        client.send_request = mock.MagicMock(return_value=self.construct_response_queues_empty())
        queues = client.get_queues()

        logger.info.assert_not_called()
        logger.error.assert_called_once()
        client.send_request.assert_called_once()
        self.assertEquals([], queues)

    def test_get_queues_returns_empty_list_when_error(self):
        logger = mock.MagicMock()
        arguments = self.construct_arguments()

        client = apiclient.ApiClient(logger, arguments)
        client.send_request = mock.MagicMock(return_value=None)
        apiclient.urllib2.build_opener.open = mock.MagicMock(side_effect=urllib2.HTTPError)
        response = client.get_queues()

        client.send_request.assert_called_once()
        self.assertEquals([], response)

    def test_get_connections_returns_result_when_no_error(self):
        logger = mock.MagicMock()
        arguments = self.construct_arguments()

        client = apiclient.ApiClient(logger, arguments)
        client.send_request = mock.MagicMock(return_value=self.construct_response_connections())
        response = client.get_connections()

        client.send_request.assert_called_once()
        self.assertEquals(self.construct_response_connections(), response)

    def test_get_connections_returns_none_when_error(self):
        logger = mock.MagicMock()
        arguments = self.construct_arguments()

        client = apiclient.ApiClient(logger, arguments)
        client.send_request = mock.MagicMock(return_value=None)
        apiclient.urllib2.build_opener.open = mock.MagicMock(side_effect=urllib2.HTTPError)
        response = client.get_connections()

        client.send_request.assert_called_once()
        self.assertEquals(None, response)

    def test_get_consumers_returns_result_when_no_error(self):
        logger = mock.MagicMock()
        arguments = self.construct_arguments()

        client = apiclient.ApiClient(logger, arguments)
        client.send_request = mock.MagicMock(return_value=self.construct_response_consumers())
        response = client.get_consumers()

        client.send_request.assert_called_once()
        self.assertEquals(self.construct_response_consumers(), response)

    def test_get_consumers_returns_none_when_error(self):
        logger = mock.MagicMock()
        arguments = self.construct_arguments()

        client = apiclient.ApiClient(logger, arguments)
        client.send_request = mock.MagicMock(return_value=None)
        apiclient.urllib2.build_opener.open = mock.MagicMock(side_effect=urllib2.HTTPError)
        response = client.get_consumers()

        client.send_request.assert_called_once()
        self.assertEquals(None, response)

    def test_get_nodes_returns_result_when_no_error(self):
        logger = mock.MagicMock()
        arguments = self.construct_arguments()

        client = apiclient.ApiClient(logger, arguments)
        client.send_request = mock.MagicMock(return_value=self.construct_response_nodes())
        response = client.get_nodes()

        client.send_request.assert_called_once()
        self.assertEquals(self.construct_response_nodes(), response)

    def test_get_nodes_returns_none_when_error(self):
        logger = mock.MagicMock()
        arguments = self.construct_arguments()

        client = apiclient.ApiClient(logger, arguments)
        client.send_request = mock.MagicMock(return_value=None)
        apiclient.urllib2.build_opener.open = mock.MagicMock(side_effect=urllib2.HTTPError)
        response = client.get_nodes()

        client.send_request.assert_called_once()
        self.assertEquals(None, response)

    def test_send_request_returns_result_when_no_error(self):
        logger = mock.MagicMock()
        arguments = self.construct_arguments()

        uri = "/api/nodes"
        url = "%s://%s:%s%s" % (arguments["server_scheme"], arguments["server_host"], arguments["server_port"], uri)

        client = apiclient.ApiClient(logger, arguments)
        apiclient.urllib2.HTTPPasswordMgrWithDefaultRealm = mock.MagicMock()
        apiclient.urllib2.build_opener = mock.MagicMock()
        apiclient.json.loads = mock.MagicMock(return_value=self.construct_response_nodes())
        response = client.send_request(uri)

        apiclient.urllib2.HTTPPasswordMgrWithDefaultRealm().add_password.assert_called_once_with(None, url, arguments["server_username"], arguments["server_password"])
        apiclient.urllib2.build_opener(mock.MagicMock()).open.assert_called_with(url)
        apiclient.json.loads.assert_called_once()
        self.assertEqual(self.construct_response_nodes(), response)
        logger.error.assert_not_called()

    def test_send_request_returns_none_when_error(self):
        logger = mock.MagicMock()
        arguments = self.construct_arguments()

        uri = "/api/nodes"
        url = "%s://%s:%s%s" % (arguments["server_scheme"], arguments["server_host"], arguments["server_port"], uri)

        client = apiclient.ApiClient(logger, arguments)
        apiclient.urllib2.build_opener.open = mock.MagicMock(side_effect=urllib2.HTTPError)
        apiclient.json.loads = mock.MagicMock(return_value=self.construct_response_nodes())
        response = client.send_request(uri)

        apiclient.json.loads.assert_not_called()
        logger.error.assert_called_once()
        self.assertEquals(None, response)

    @staticmethod
    def construct_arguments():
        arguments = {
            "server_scheme": "http",
            "server_host": "foo-host",
            "server_port": 1,
            "server_host_alias": "bar-host",
            "server_username": "user",
            "server_password": "pass",
            "server_vhost": "foo",
            "server_queue": "foo",
            "server_queues": ["foo"],
            "server_queues_discovery": False,
            "generic_conditions": {
                "conditions_consumers_connected": 1,
                "conditions_open_connections": 1,
                "conditions_nodes_running": 1,
                "conditions_node_memory_used": 1
            },
            "conditions": {
                "foo": {
                    "conditions_ready_queue_size": 0,
                    "conditions_unack_queue_size": 0,
                    "conditions_total_queue_size": 0,
                    "conditions_queue_consumers_connected": 0,
                }
            },
            "email_to": ["foo@foobar.com"],
            "email_from": "bar@foobar.com",
            "email_subject": "foo %s %s",
            "email_server": "mail.foobar.com",
            "email_password": "",
            "email_ssl": False,
            "slack_url": "http://foo.com",
            "slack_channel": "channel",
            "slack_username": "username",
            "telegram_bot_id": "foo_bot",
            "telegram_channel": "foo_channel",
            "teams_webhook": "http://foo.com/webhook"
        }

        return arguments

    @staticmethod
    def construct_response_queue():
        return {
            "messages_ready": 0,
            "messages_unacknowledged": 0,
            "messages": 0,
            "consumers": 0
        }

    @staticmethod
    def construct_response_queues():
        return {
            "page_count": 1,
            "page_size": 300,
            "page": 1,
            "filtered_count": 2,
            "item_count": 2,
            "total_count": 2,
            "items": [
                { "name": "foo" },
                { "name": "bar" }
            ]
        }

    @staticmethod
    def construct_response_queues_empty():
        return {
            "page_count": 1,
            "page_size": 300,
            "page": 1,
            "filtered_count": 0,
            "item_count": 0,
            "total_count": 0,
            "items": []
        }

    @staticmethod
    def construct_response_connections():
        return {
            "connection_foo": {},
            "connection_bar": {}
        }

    @staticmethod
    def construct_response_consumers():
        return {
            "consumer_foo": {},
            "consumer_bar": {}
        }

    @staticmethod
    def construct_response_nodes():
        return [
            { "mem_used": 500000 },
            { "mem_used": 500000 }
        ]


if __name__ == "__main__":
    unittest.main()
