import pytest
from httpx import AsyncClient



# @pytest.mark.parametrize("room_id,date_from,date_to,status_code", [
#     *[(4,"2030-05-01","2030-05-15",200)]*8,
#     (4,"2030-05-01","2030-05-15",409),
#     (4,"2030-05-01","2030-05-15",409)
# ])
# async def test_add_and_get_bookings(room_id,date_from,date_to,status_code,authenticated_ac:AsyncClient):
#     response = await authenticated_ac.post("/bookings/add",json ={
#         "room_id":room_id,
#         "date_from":date_from,
#         "date_to":date_to,
#     })
#
#
#     assert response.status_code == status_code
#
#
#
#
# @pytest.mark.parametrize("room_id,date_from,date_to,status_code", [
#     (3,"2030-05-15","2030-05-15",400),
#     (3,"2030-05-01","2030-06-15",400),
#     (3,"2030-05-01","2030-05-15",200)
# ])
# async def test_date_from_date_to(room_id,date_from,date_to,status_code,authenticated_ac:AsyncClient):
#     response = await authenticated_ac.post("/bookings/add",json ={
#         "room_id":room_id,
#         "date_from":date_from,
#         "date_to":date_to,
#     })
#
#     assert response.status_code == status_code
# #


@pytest.mark.parametrize("id,user_id,status_code",[
    (1,1,200),
    (2,1,200),


])
async def test_get_del_bookings(id,user_id,status_code,authenticated_ac:AsyncClient):
    before_response = await authenticated_ac.get("/bookings")
    assert before_response.status_code == status_code
    assert before_response.json() is not None

    delete_response = await authenticated_ac.delete("/bookings/del",params={
        "id":id,
        "user_id":user_id
    })
    assert delete_response.status_code == status_code

    response_after = await authenticated_ac.get("/bookings")
    assert response_after.status_code == status_code

    print(response_after.json(),'After Response')
#
