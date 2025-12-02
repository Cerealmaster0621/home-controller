//
//  Config.swift
//  HomeController
//
//  Configuration file for backend API
//

import Foundation

enum Config {
    // Backend URL is now loaded from Secrets.swift (gitignored)
    // To configure: Copy Secrets.swift.example to Secrets.swift and add your IP
    static let baseURL = Secrets.backendURL
    
    // API endpoints
    enum API {
        static let ac = "/ac"
        static let light = "/light"
    }
}

