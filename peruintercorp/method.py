import pusher
import frappe
def pusherev(doc,event):

	pusher_client = pusher.Pusher(
		app_id='1494462',
		key='bf123e34088bf8575c3a',
		secret='fbd2d928ab5762cb9cc4',
		cluster='sa1',
		ssl=True
	)
	fr = frappe.get_doc('ChatCorp Rooms',doc.room)
	
	for user in fr.room_users:
		if doc.owner!=user.chatcorp_user:
			pusher_client.trigger(user.chatcorp_user, 'message',{
				"room":"c160m9b7l3",
				"obj":{"chat_message":"<div class=\"recive\">"+doc.message+"</div>"}
})