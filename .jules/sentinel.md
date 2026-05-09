## 2024-05-09 - Mass Assignment in Update Endpoints
**Vulnerability:** Mass assignment in the `update_task` and `update_note` endpoints allowed users to arbitrarily modify any fields in the object, such as the generated `id` or `created_at` timestamp.
**Learning:** The previous implementation blindly passed the entire parsed JSON body from `request.get_json()` directly into `dict.update(data)`. This pattern of implicitly trusting all incoming data is dangerous.
**Prevention:** Always use explicit field whitelisting when updating objects based on user input, defining exactly which fields are safe to be modified and only applying those to the stored object.
