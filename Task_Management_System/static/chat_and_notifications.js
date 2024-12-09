











// // Replace with dynamic task ID in production
// const taskId = 1;
// console.log("Task ID :" +taskId);
// // WebSocket for chat
// const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${taskId}/`);
// console.log(chatSocket);
// chatSocket.onmessage = function (e) {
//     const data = JSON.parse(e.data);
//     const chatBox = document.getElementById('chat-box');

//     // Append new chat message
//     const newMessage = document.createElement('div');
//     newMessage.innerHTML = `
//         <p>
//             <strong>${data.sender}:</strong> ${data.message} 
//             <span class="text-muted" style="font-size: 0.8em;">(${data.timestamp})</span>
//         </p>
//     `;
//     chatBox.appendChild(newMessage);

//     // Auto-scroll to the bottom
//     chatBox.scrollTop = chatBox.scrollHeight;
// };

// chatSocket.onclose = function () {
//     console.error('Chat WebSocket closed unexpectedly.');
// };

// // Handle chat form submission
// document.getElementById('chat-form').addEventListener('submit', function (e) {
//     e.preventDefault();

//     const messageInput = document.getElementById('chat-message');
//     const message = messageInput.value;

//     if (message.trim() !== '') {
//         chatSocket.send(JSON.stringify({
//             'message': message
//         }));
//         messageInput.value = '';
//     }
// });

// // WebSocket for notifications
// const notificationSocket = new WebSocket(`ws://${window.location.host}/ws/notifications/`);

// notificationSocket.onmessage = function (e) {
//     const data = JSON.parse(e.data);

//     // Add notification to the list
//     const notificationsList = document.getElementById('notifications');
//     const newNotification = document.createElement('li');
//     newNotification.className = 'list-group-item';
//     newNotification.textContent = data.message;
//     notificationsList.insertBefore(newNotification, notificationsList.firstChild);
// };

// notificationSocket.onclose = function () {
//     console.error('Notification WebSocket closed unexpectedly.');
// };
