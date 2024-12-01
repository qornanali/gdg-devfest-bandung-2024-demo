import 'package:flutter/material.dart';
import '../services/chat_service.dart';
import '../widgets/message_list.dart';
import '../widgets/message_input.dart';

class ChatPage extends StatefulWidget {
  final ChatService chatService;

  const ChatPage({super.key, required this.chatService});

  @override
  State<ChatPage> createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  final TextEditingController _controller = TextEditingController();
  final List<Map<String, dynamic>> _messages = [];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Tanya Tanya'),
      ),
      body: Column(
        children: [
          MessageList(messages: _messages),
          MessageInput(
            controller: _controller,
            onSend: (message) => _sendMessage(message),
          ),
        ],
      ),
    );
  }

  Future<void> _sendMessage(String message) async {
    final timestamp = DateTime.now().millisecondsSinceEpoch;

    setState(() {
      _messages
          .add({'sender': 'You', 'text': message, 'created_time': timestamp});
    });

    final botResponse = await widget.chatService.sendMessage(message);
    setState(() {
      _messages.add({
        'sender': 'Bot',
        'text': botResponse['message'],
        'created_time': botResponse['created_time']
      });
    });

    _controller.clear();
  }
}
