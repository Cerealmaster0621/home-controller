//
//  NetworkService.swift
//  HomeController
//
//  Singleton service for handling API requests
//

import Foundation

class NetworkService {
    // MARK: - Singleton
    static let shared = NetworkService()
    
    private init() {}
    
    // MARK: - Private Properties
    private let baseURL = Config.baseURL
    
    // MARK: - Public Methods
    
    /// Generic POST request handler
    private func post<T: Codable>(endpoint: String) async throws -> T {
        guard let url = URL(string: baseURL + endpoint) else {
            throw NetworkError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse
        }
        
        guard (200...299).contains(httpResponse.statusCode) else {
            if let errorResponse = try? JSONDecoder().decode(ErrorResponse.self, from: data) {
                throw NetworkError.serverError(errorResponse.detail)
            }
            throw NetworkError.statusCode(httpResponse.statusCode)
        }
        
        do {
            let decodedResponse = try JSONDecoder().decode(T.self, from: data)
            return decodedResponse
        } catch {
            throw NetworkError.decodingError(error)
        }
    }
    
    // MARK: - AC Control Methods
    
    func turnOnAircon() async throws -> ACResponse {
        try await post(endpoint: "\(Config.API.ac)/aircon/on")
    }
    
    func turnOnHeater() async throws -> ACResponse {
        try await post(endpoint: "\(Config.API.ac)/heater/on")
    }
    
    func turnOffAC() async throws -> ACResponse {
        try await post(endpoint: "\(Config.API.ac)/off")
    }
    
    func increaseAirconTemp() async throws -> ACResponse {
        try await post(endpoint: "\(Config.API.ac)/aircon/temp/up")
    }
    
    func increaseHeaterTemp() async throws -> ACResponse {
        try await post(endpoint: "\(Config.API.ac)/heater/temp/up")
    }
    
    func decreaseHeaterTemp() async throws -> ACResponse {
        try await post(endpoint: "\(Config.API.ac)/heater/temp/down")
    }
    
    func turnOnTimer() async throws -> ACResponse {
        try await post(endpoint: "\(Config.API.ac)/timer/on")
    }
    
    func increaseTimer() async throws -> ACResponse {
        try await post(endpoint: "\(Config.API.ac)/timer/up")
    }
    
    func decreaseTimer() async throws -> ACResponse {
        try await post(endpoint: "\(Config.API.ac)/timer/down")
    }
    
    // MARK: - Light Control Methods
    
    func setLightAllBright() async throws -> LightResponse {
        try await post(endpoint: "\(Config.API.light)/all-bright")
    }
    
    func setLightBright() async throws -> LightResponse {
        try await post(endpoint: "\(Config.API.light)/bright")
    }
    
    func setLightDark() async throws -> LightResponse {
        try await post(endpoint: "\(Config.API.light)/dark")
    }
    
    func turnOnLight() async throws -> LightResponse {
        try await post(endpoint: "\(Config.API.light)/on")
    }
    
    func turnOffLight() async throws -> LightResponse {
        try await post(endpoint: "\(Config.API.light)/off")
    }
}

// MARK: - Network Errors

enum NetworkError: LocalizedError {
    case invalidURL
    case invalidResponse
    case statusCode(Int)
    case serverError(String)
    case decodingError(Error)
    
    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid URL"
        case .invalidResponse:
            return "Invalid response from server"
        case .statusCode(let code):
            return "Server returned status code: \(code)"
        case .serverError(let message):
            return message
        case .decodingError(let error):
            return "Decoding error: \(error.localizedDescription)"
        }
    }
}

