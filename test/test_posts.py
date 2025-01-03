import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from typing import List
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    
    def validate(post):
        return schemas.PostOut(**post)
    post_map = map(validate, res.json())
    post_list = list(post_map)
    print(list(post_map))

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_nonexistent_posts(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/635318")
    assert res.status_code == 404

def test_get_one_post(authorized_client,test_posts):
     res = authorized_client.get(f"/posts/{test_posts[0].id}")
     post = schemas.PostOut(**res.json())
     assert post.Post.id == test_posts[0].id
     assert post.Post.content == test_posts[0].content
     assert post.Post.title == test_posts[0].title

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),

])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

def test_unauthorized_user_create_post(client, test_posts, test_user):
    res = client.post("/posts/", json={"title": "random title", "content": "aasdfttghy"})
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_posts,test_user):
    res = client.delete(f"/posts/{test_posts[0].id}" )
    assert res.status_code == 401

def test_delete_succes(authorized_client, test_posts, test_user):
    res= authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_nonexist(authorized_client,test_posts,test_user):
    res = authorized_client.delete(f"/posts/8000")
    assert res.status_code == 404

def test_del_other_usr_post(authorized_client ,test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update(authorized_client,test_posts,test_user):
    data = {"title": "updated title",
            "content": "updaated content",
            "id": test_posts[0].id
            }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]

def test_update_other_usr_post(authorized_client ,test_posts,test_user, test_user2):
    data = {"title": "updated title",
            "content": "updaated content",
            "id": test_posts[3].id
            }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

    

def test_update_unauthorized_usr_post(client,test_posts,test_user):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_update_post_nonexist(authorized_client,test_posts,test_user):
    data = {"title": "updated title",
            "content": "updaated content",
            "id": test_posts[3].id
            }
    res = authorized_client.put(f"/posts/6513", json=data)
    assert res.status_code == 404



