//
//  APIModels.swift
//  HomeController
//
//  Models for API responses
//

import Foundation

// MARK: - AC Models

struct ACResponse: Codable {
    let success: Bool
    let message: String
    let mode: String?
    let control: String?
}

struct ACStatusResponse: Codable {
    let available_modes: [String]
    let available_temp_controls: [String]
    let available_timer_controls: [String]
}

// MARK: - Light Models

struct LightResponse: Codable {
    let success: Bool
    let message: String
    let mode: String
}

// MARK: - Error Response

struct ErrorResponse: Codable {
    let detail: String
}

