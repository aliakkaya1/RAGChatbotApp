// APIService.swift

import Foundation

// 1. Define the data structures that match our backend's JSON
// 'Codable' allows Swift to easily convert these structs to and from JSON data.
struct ChatRequest: Codable {
    let query: String
}

struct ChatResponse: Codable {
    let answer: String
    let source: String?
}

// 2. Create a dedicated class for our API service
class APIService {
    // The main function that sends the message to the backend
    func sendMessage(message: String) async throws -> String {
        // The URL of your local FastAPI server
        let url = URL(string: "http://127.0.0.1:8000/chat")!
        
        // 3. Prepare the request
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        // Encode the user's message into JSON data
        let chatRequest = ChatRequest(query: message)
        request.httpBody = try JSONEncoder().encode(chatRequest)
        
        // 4. Send the request and wait for a response
        // 'URLSession' is Apple's framework for networking.
        let (data, _) = try await URLSession.shared.data(for: request)
        
        // 5. Decode the JSON response from the backend
        let chatResponse = try JSONDecoder().decode(ChatResponse.self, from: data)
        
        // Return the chatbot's answer
        return chatResponse.answer
    }
}
