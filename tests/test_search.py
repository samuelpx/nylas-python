import json
import pytest
import responses

@pytest.fixture
def mock_thread_search_response(api_url):
    snippet = (
        "Hey Helena, Looking forward to getting together for dinner on Friday. "
        "What can I bring? I have a couple bottles of wine or could put together"
    )
    response_body = json.dumps([
        {
            "id": "evh5uy0shhpm5d0le89goor17",
            "object": "thread",
            "account_id": "awa6ltos76vz5hvphkp8k17nt",
            "subject": "Dinner Party on Friday",
            "unread": False,
            "starred": False,
            "last_message_timestamp": 1398229259,
            "last_message_received_timestamp": 1398229259,
            "first_message_timestamp": 1298229259,
            "participants": [
                {
                    "name": "Ben Bitdiddle",
                    "email": "ben.bitdiddle@gmail.com"
                },
            ],
            "snippet": snippet,
            "folders": [
                {
                    "name": "inbox",
                    "display_name": "INBOX",
                    "id": "f0idlvozkrpj3ihxze7obpivh"
                },
            ],
            "message_ids": [
                "251r594smznew6yhiocht2v29",
                "7upzl8ss738iz8xf48lm84q3e",
                "ah5wuphj3t83j260jqucm9a28"
            ],
            "draft_ids": [
                "251r594smznew6yhi12312saq"
            ],
            "version": 2
        }
    ])

    responses.add(
        responses.GET,
        api_url + '/threads/search?q=Helena',
        body=response_body,
        status=200,
        content_type='application/json',
        match_querystring=True
    )

@pytest.fixture
def mock_message_search_response(api_url):
    snippet = (
        "Sounds good--that bottle of Pinot should go well with the meal. "
        "I'll also bring a surprise for dessert. :) "
        "Do you have ice cream? Looking fo"
    )
    response_body = json.dumps([
        {
            "id": "84umizq7c4jtrew491brpa6iu",
            "object": "message",
            "account_id": "14e5bn96uizyuhidhcw5rfrb0",
            "thread_id": "5vryyrki4fqt7am31uso27t3f",
            "subject": "Re: Dinner on Friday?",
            "from": [
                {
                    "name": "Ben Bitdiddle",
                    "email": "ben.bitdiddle@gmail.com"
                }
            ],
            "to": [
                {
                    "name": "Bill Rogers",
                    "email": "wbrogers@mit.edu"
                }
            ],
            "cc": [],
            "bcc": [],
            "reply_to": [],
            "date": 1370084645,
            "unread": True,
            "starred": False,
            "folder": {
                "name": "inbox",
                "display_name": "INBOX",
                "id": "f0idlvozkrpj3ihxze7obpivh"
            },
            "snippet": snippet,
            "body": "<html><body>....</body></html>",
            "files": [],
            "events": []
        },
        {
            "id": "84umizq7asdf3aw491brpa6iu",
            "object": "message",
            "account_id": "14e5bakdsfljskidhcw5rfrb0",
            "thread_id": "5vryyralskdjfwlj1uso27t3f",
            "subject": "Re: Dinner on Friday?",
            "from": [
                {
                    "name": "Ben Bitdiddle",
                    "email": "ben.bitdiddle@gmail.com"
                }
            ],
            "to": [
                {
                    "name": "Bill Rogers",
                    "email": "wbrogers@mit.edu"
                }
            ],
            "cc": [],
            "bcc": [],
            "reply_to": [],
            "date": 1370084645,
            "unread": True,
            "starred": False,
            "folder": {
                "name": "inbox",
                "display_name": "INBOX",
                "id": "f0idlvozkrpj3ihxze7obpivh"
            },
            "snippet": snippet,
            "body": "<html><body>....</body></html>",
            "files": [],
            "events": []
        }
    ])

    responses.add(
        responses.GET,
        api_url + '/messages/search?q=Pinot',
        body=response_body,
        status=200,
        content_type='application/json',
        match_querystring=True
    )


@responses.activate
@pytest.mark.usefixtures("mock_thread_search_response")
def test_search_threads(api_client):
    threads = api_client.threads.search("Helena")
    assert len(threads) == 1
    assert "Helena" in threads[0].snippet

@responses.activate
@pytest.mark.usefixtures("mock_message_search_response")
def test_search_messages(api_client):
    messages = api_client.messages.search("Pinot")
    assert len(messages) == 2
    assert "Pinot" in messages[0].snippet
    assert "Pinot" in messages[1].snippet

@responses.activate
@pytest.mark.usefixtures("mock_message_search_response")
def test_search_drafts(api_client):
    with pytest.raises(Exception):
        api_client.drafts.search("Pinot")
