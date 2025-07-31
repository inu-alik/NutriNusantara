import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(NutriNusantaraApp());
}

class NutriNusantaraApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'NutriNusantara',
      theme: ThemeData(primarySwatch: Colors.green),
      home: RegisterScreen(),
    );
  }
}

class RegisterScreen extends StatefulWidget {
  @override
  _RegisterScreenState createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();
  String username = '', gender = 'male', activity = 'sedentari', goal = 'menurunkan';
  int age = 20;
  double weight = 60, height = 170;

  void _register() async {
    var response = await http.post(
      Uri.parse('http://localhost:5000/register'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'username': username,
        'gender': gender,
        'age': age,
        'weight': weight,
        'height': height,
        'activity_level': activity,
        'goal': goal,
      }),
    );
    if (response.statusCode == 201) {
      var userId = jsonDecode(response.body)['user_id'];
      Navigator.push(
        context,
        MaterialPageRoute(builder: (context) => HomeScreen(userId: userId)),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Registrasi Pengguna')),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: EdgeInsets.all(16),
          children: [
            TextFormField(
              decoration: InputDecoration(labelText: 'Username'),
              onChanged: (v) => username = v,
            ),
            DropdownButtonFormField(
              value: gender,
              items: ['male', 'female'].map((g) => DropdownMenuItem(value: g, child: Text(g))).toList(),
              onChanged: (v) => setState(() => gender = v!),
              decoration: InputDecoration(labelText: 'Gender'),
            ),
            TextFormField(
              decoration: InputDecoration(labelText: 'Usia'),
              keyboardType: TextInputType.number,
              onChanged: (v) => age = int.tryParse(v) ?? 0,
            ),
            TextFormField(
              decoration: InputDecoration(labelText: 'Berat (kg)'),
              keyboardType: TextInputType.number,
              onChanged: (v) => weight = double.tryParse(v) ?? 0,
            ),
            TextFormField(
              decoration: InputDecoration(labelText: 'Tinggi (cm)'),
              keyboardType: TextInputType.number,
              onChanged: (v) => height = double.tryParse(v) ?? 0,
            ),
            DropdownButtonFormField(
              value: activity,
              items: ['sedentari', 'ringan', 'sedang', 'berat'].map((a) => DropdownMenuItem(value: a, child: Text(a))).toList(),
              onChanged: (v) => setState(() => activity = v!),
              decoration: InputDecoration(labelText: 'Aktivitas'),
            ),
            DropdownButtonFormField(
              value: goal,
              items: ['menurunkan', 'menjaga', 'menaikkan'].map((g) => DropdownMenuItem(value: g, child: Text(g))).toList(),
              onChanged: (v) => setState(() => goal = v!),
              decoration: InputDecoration(labelText: 'Tujuan'),
            ),
            SizedBox(height: 16),
            ElevatedButton(onPressed: _register, child: Text('Daftar')),
          ],
        ),
      ),
    );
  }
}

class HomeScreen extends StatelessWidget {
  final int userId;
  HomeScreen({required this.userId});

  Future<int?> fetchCalorieTarget() async {
    var response = await http.get(Uri.parse('http://localhost:5000/calorie_target/$userId'));
    if (response.statusCode == 200) {
      var data = jsonDecode(response.body);
      return data['calorie_target'];
    }
    return null;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Beranda')),
      body: FutureBuilder<int?>(
        future: fetchCalorieTarget(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting)
            return Center(child: CircularProgressIndicator());
          if (!snapshot.hasData)
            return Center(child: Text('Gagal memuat target kalori'));
          return Center(
            child: Text('Target Kalori Harian Anda: ${snapshot.data} kkal', style: TextStyle(fontSize: 24)),
          );
        },
      ),
    );
  }
}