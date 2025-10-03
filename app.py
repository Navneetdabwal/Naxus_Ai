from flask import Flask, request, jsonify, render_template_string
import requests
from urllib.parse import quote
import json
from base64 import b64encode
import os
import uuid
from datetime import datetime

app = Flask(__name__)

# API Keys and Endpoints
GPT5_API_URL = 'https://apis.prexzyvilla.site/ai/gpt5'
POLL_IMAGE_URL = 'https://image.pollinations.ai/prompt'
OPENROUTER_API_KEY_GROK = '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'
OPENROUTER_API_KEY_QWEN = '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'
OPENROUTER_BASE_URL = 'https://openrouter.ai/api/v1/chat/completions'
SAMBANOVA_API_KEY = '4ec0f0b9-8578-41da-b7d5-c8d0e3a321b3'
SAMBANOVA_API_URL = 'https://api.sambanova.ai/v1/chat/completions'
TRAXDINOSAUR_API_URL = 'https://apiimagestrax.vercel.app/api/genimage'
TRAXBG_API_URL = 'https://apirmbgtrax.vercel.app/remove-bg'
PREXZY_IMAGE_URL = 'https://apis.prexzyvilla.site/ai/imagen'

# Create uploads directory
os.makedirs('static/uploads', exist_ok=True)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚡ Nexus AI Pro</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800&family=Rajdhani:wght@300;400;500;600;700&family=Exo+2:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #6a00ff;
            --primary-glow: #8a2be2;
            --secondary: #ff00ff;
            --accent: #00ffff;
            --dark: #0a0a1f;
            --darker: #050510;
            --light: #1a1a3a;
            --lighter: #25254d;
            --text: #e6e6ff;
            --text-light: #b8b8ff;
            --success: #00ff88;
            --warning: #ffaa00;
            --error: #ff4444;
            --glass: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
            --neon-glow: 0 0 10px, 0 0 20px, 0 0 30px;
        }
        [data-theme="light"] {
            --dark: #f0f0ff;
            --darker: #e0e0ff;
            --light: #ffffff;
            --lighter: #f5f5ff;
            --text: #333366;
            --text-light: #666699;
            --glass: rgba(106, 0, 255, 0.05);
            --glass-border: rgba(106, 0, 255, 0.1);
        }
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Exo 2', sans-serif;
            background: linear-gradient(135deg, var(--darker), var(--dark));
            color: var(--text);
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background:
                radial-gradient(circle at 20% 80%, var(--primary) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, var(--secondary) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, var(--accent) 0%, transparent 50%);
            opacity: 0.1;
            z-index: -1;
            animation: backgroundShift 20s ease-in-out infinite alternate;
        }
        @keyframes backgroundShift {
            0% { transform: scale(1) rotate(0deg); }
            100% { transform: scale(1.1) rotate(180deg); }
        }
        .cyber-grid {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background:
                linear-gradient(90deg, var(--glass-border) 1px, transparent 1px) 0 0 / 50px 50px,
                linear-gradient(0deg, var(--glass-border) 1px, transparent 1px) 0 0 / 50px 50px;
            opacity: 0.3;
            z-index: -1;
            animation: gridMove 20s linear infinite;
        }
        @keyframes gridMove {
            0% { transform: translate(0, 0); }
            100% { transform: translate(50px, 50px); }
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            min-height: 100vh;
        }
        /* Header Styles */
        .header {
            text-align: center;
            margin-bottom: 30px;
            position: relative;
            padding: 40px 0;
        }
        .main-title {
            font-family: 'Orbitron', monospace;
            font-size: 4rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary), var(--secondary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: var(--neon-glow) var(--primary);
            margin-bottom: 10px;
            animation: titlePulse 3s ease-in-out infinite;
            letter-spacing: 3px;
        }
        @keyframes titlePulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }
        .subtitle {
            font-family: 'Rajdhani', sans-serif;
            font-size: 1.3rem;
            color: var(--text-light);
            font-weight: 300;
            letter-spacing: 2px;
        }
        /* Control Bar */
        .control-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 15px 25px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        .theme-toggle {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border: none;
            color: white;
            padding: 12px 20px;
            border-radius: 15px;
            cursor: pointer;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 0 20px var(--primary);
        }
        .theme-toggle:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 30px var(--secondary);
        }
        .model-selector {
            display: flex;
            gap: 15px;
            align-items: center;
        }
        .model-btn {
            background: var(--glass);
            border: 1px solid var(--glass-border);
            color: var(--text);
            padding: 10px 20px;
            border-radius: 12px;
            cursor: pointer;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 500;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .model-btn.active {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            box-shadow: 0 0 20px var(--primary);
        }
        .model-btn:hover {
            transform: translateY(-2px);
            border-color: var(--primary);
        }
        /* Main Layout */
        .main-layout {
            display: grid;
            grid-template-columns: 300px 1fr;
            gap: 25px;
            height: calc(100vh - 200px);
        }
        /* Sidebar */
        .sidebar {
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            display: flex;
            flex-direction: column;
        }
        .sidebar-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid var(--glass-border);
        }
        .sidebar-title {
            font-family: 'Orbitron', monospace;
            font-size: 1.3rem;
            color: var(--accent);
            font-weight: 600;
        }
        .new-chat-btn {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border: none;
            color: white;
            padding: 10px 15px;
            border-radius: 10px;
            cursor: pointer;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 600;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .new-chat-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 20px var(--primary);
        }
        .chat-list {
            flex: 1;
            overflow-y: auto;
        }
        .chat-item {
            background: var(--glass);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }
        .chat-item::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
            transition: left 0.5s;
        }
        .chat-item:hover::before {
            left: 100%;
        }
        .chat-item.active {
            background: linear-gradient(135deg, var(--primary), transparent);
            border-color: var(--primary);
            box-shadow: 0 0 20px var(--primary);
        }
        .chat-item:hover {
            transform: translateX(5px);
            border-color: var(--accent);
        }
        .chat-content {
            flex: 1;
        }
        .chat-name {
            font-weight: 600;
            margin-bottom: 5px;
            color: var(--text);
        }
        .chat-preview {
            font-size: 0.85rem;
            color: var(--text-light);
            opacity: 0.8;
        }
        .chat-time {
            font-size: 0.75rem;
            color: var(--accent);
            margin-top: 5px;
        }
        .chat-actions {
            display: flex;
            gap: 5px;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        .chat-item:hover .chat-actions {
            opacity: 1;
        }
        .chat-action-btn {
            background: none;
            border: none;
            color: var(--text-light);
            cursor: pointer;
            font-size: 0.8rem;
            padding: 2px 5px;
            border-radius: 4px;
            transition: all 0.3s ease;
        }
        .chat-action-btn:hover {
            color: var(--primary);
            background: rgba(106, 0, 255, 0.1);
        }
        /* Modal Styles */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(10px);
            animation: fadeIn 0.3s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .modal-content {
            background: var(--glass);
            backdrop-filter: blur(20px);
            margin: 15% auto;
            padding: 30px;
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            width: 90%;
            max-width: 400px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            animation: slideIn 0.3s ease;
        }
        @keyframes slideIn {
            from { transform: translateY(-50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        .modal-header {
            font-family: 'Orbitron', monospace;
            font-size: 1.5rem;
            color: var(--accent);
            margin-bottom: 15px;
        }
        .modal-body {
            color: var(--text);
            margin-bottom: 20px;
            line-height: 1.5;
        }
        .modal-input {
            width: 100%;
            background: var(--dark);
            border: 1px solid var(--glass-border);
            border-radius: 10px;
            padding: 12px;
            color: var(--text);
            font-family: 'Exo 2', sans-serif;
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }
        .modal-input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 10px var(--primary);
        }
        .modal-buttons {
            display: flex;
            gap: 10px;
            justify-content: center;
        }
        .modal-btn {
            padding: 10px 20px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 600;
            transition: all 0.3s ease;
            min-width: 100px;
        }
        .modal-btn-primary {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
        }
        .modal-btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px var(--primary);
        }
        .modal-btn-secondary {
            background: var(--glass);
            color: var(--text);
            border: 1px solid var(--glass-border);
        }
        .modal-btn-secondary:hover {
            background: var(--light);
            transform: translateY(-2px);
        }
        .close {
            color: var(--text-light);
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
            position: absolute;
            right: 15px;
            top: 10px;
        }
        .close:hover {
            color: var(--error);
        }
        /* Main Content */
        .main-content {
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            display: flex;
            flex-direction: column;
            height: 100%;
        }
        .tab-header {
            display: flex;
            background: var(--light);
            border-radius: 20px 20px 0 0;
            padding: 0 25px;
            border-bottom: 1px solid var(--glass-border);
        }
        .tab-btn {
            padding: 20px 30px;
            background: transparent;
            border: none;
            color: var(--text-light);
            font-family: 'Rajdhani', sans-serif;
            font-weight: 600;
            font-size: 1.1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .tab-btn.active {
            color: var(--accent);
        }
        .tab-btn.active::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            border-radius: 3px 3px 0 0;
        }
        .tab-btn:hover {
            color: var(--text);
            transform: translateY(-2px);
        }
        .tab-content {
            flex: 1;
            padding: 25px;
            overflow-y: auto;
            display: none;
        }
        .tab-content.active {
            display: block;
            animation: fadeIn 0.5s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        /* Chat Styles */
        .chat-container {
            height: 500px;
            overflow-y: auto;
            padding: 20px;
            background: var(--dark);
            border-radius: 15px;
            border: 1px solid var(--glass-border);
            margin-bottom: 20px;
            position: relative;
        }
        .loading-message {
            text-align: center;
            padding: 20px;
            color: var(--accent);
            font-style: italic;
        }
        .loading-spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid var(--glass-border);
            border-radius: 50%;
            border-top-color: var(--accent);
            animation: spin 1s ease-in-out infinite;
            margin-right: 10px;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        .message {
            margin: 20px 0;
            padding: 20px;
            border-radius: 20px;
            max-width: 80%;
            position: relative;
            animation: messageSlide 0.3s ease;
            line-height: 1.6;
        }
        @keyframes messageSlide {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .user-message {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            margin-left: auto;
            border-radius: 20px 20px 5px 20px;
            box-shadow: 0 5px 20px rgba(106, 0, 255, 0.3);
        }
        .bot-message {
            background: var(--light);
            border: 1px solid var(--glass-border);
            border-radius: 20px 20px 20px 5px;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        }
        .message-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
            font-weight: 600;
            font-size: 0.9rem;
        }
        .user-message .message-header {
            color: rgba(255,255,255,0.9);
        }
        .bot-message .message-header {
            color: var(--accent);
        }
        .input-area {
            display: flex;
            gap: 15px;
            align-items: flex-end;
        }
        .message-input {
            flex: 1;
            background: var(--dark);
            border: 1px solid var(--glass-border);
            border-radius: 15px;
            padding: 18px 20px;
            color: var(--text);
            font-family: 'Exo 2', sans-serif;
            font-size: 1rem;
            resize: none;
            height: 60px;
            transition: all 0.3s ease;
        }
        .message-input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 20px var(--primary);
        }
        .send-btn {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border: none;
            color: white;
            padding: 18px 25px;
            border-radius: 15px;
            cursor: pointer;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
            min-width: 120px;
            justify-content: center;
        }
        .send-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 25px var(--primary);
        }
        .send-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        /* Image Generation Styles */
        .image-controls {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 25px;
        }
        .control-group {
            background: var(--dark);
            border: 1px solid var(--glass-border);
            border-radius: 15px;
            padding: 20px;
        }
        .control-label {
            display: block;
            margin-bottom: 10px;
            font-weight: 600;
            color: var(--accent);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .prompt-area {
            grid-column: 1 / -1;
        }
        .prompt-input {
            width: 100%;
            min-height: 120px;
            background: var(--dark);
            border: 1px solid var(--glass-border);
            border-radius: 15px;
            padding: 20px;
            color: var(--text);
            font-family: 'Exo 2', sans-serif;
            font-size: 1rem;
            resize: vertical;
            transition: all 0.3s ease;
        }
        .prompt-input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 20px var(--primary);
        }
        .generate-btn {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border: none;
            color: white;
            padding: 18px 40px;
            border-radius: 15px;
            cursor: pointer;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 20px auto;
        }
        .generate-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 30px var(--primary);
        }
        .image-results {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 25px;
        }
        .image-card {
            background: var(--dark);
            border: 1px solid var(--glass-border);
            border-radius: 15px;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        .image-card:hover {
            transform: translateY(-5px);
            border-color: var(--primary);
            box-shadow: 0 10px 30px rgba(106, 0, 255, 0.3);
        }
        .image-preview {
            width: 100%;
            height: 250px;
            object-fit: cover;
            border-bottom: 1px solid var(--glass-border);
        }
        .image-actions {
            padding: 15px;
            display: flex;
            gap: 10px;
        }
        .image-btn {
            flex: 1;
            padding: 10px;
            border: 1px solid var(--glass-border);
            background: var(--light);
            color: var(--text);
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 5px;
            font-size: 0.9rem;
        }
        .image-btn:hover {
            background: var(--primary);
            color: white;
            transform: translateY(-2px);
        }
        /* BG Remover Styles */
        .upload-zone {
            border: 3px dashed var(--glass-border);
            border-radius: 20px;
            padding: 60px 40px;
            text-align: center;
            background: var(--dark);
            transition: all 0.3s ease;
            cursor: pointer;
            margin-bottom: 25px;
            position: relative;
            overflow: hidden;
        }
        .upload-zone::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(106, 0, 255, 0.1), transparent);
            transition: left 0.5s;
        }
        .upload-zone:hover::before {
            left: 100%;
        }
        .upload-zone:hover {
            border-color: var(--primary);
            background: rgba(106, 0, 255, 0.05);
        }
        .upload-zone.dragover {
            border-color: var(--success);
            background: rgba(0, 255, 136, 0.1);
        }
        .upload-icon {
            font-size: 4rem;
            color: var(--primary);
            margin-bottom: 20px;
            opacity: 0.7;
        }
        .upload-text {
            font-size: 1.3rem;
            color: var(--text);
            margin-bottom: 10px;
            font-weight: 600;
        }
        .upload-subtext {
            color: var(--text-light);
            font-size: 1rem;
        }
        .file-input {
            display: none;
        }
        .preview-area {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
            margin-top: 30px;
        }
        .preview-card {
            background: var(--dark);
            border: 1px solid var(--glass-border);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
        }
        .preview-title {
            font-weight: 600;
            color: var(--accent);
            margin-bottom: 15px;
            font-size: 1.1rem;
        }
        .preview-image {
            max-width: 100%;
            max-height: 300px;
            border-radius: 10px;
            border: 1px solid var(--glass-border);
        }
        .action-btn {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border: none;
            color: white;
            padding: 15px 30px;
            border-radius: 12px;
            cursor: pointer;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 20px auto;
        }
        .action-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 25px var(--primary);
        }
        .another-btn {
            background: linear-gradient(135deg, var(--success), var(--success));
            border: none;
            color: white;
            padding: 15px 30px;
            border-radius: 12px;
            cursor: pointer;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 20px auto;
        }
        .another-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 25px var(--success);
        }
        /* Utility Classes */
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid var(--glass-border);
            border-radius: 50%;
            border-top-color: var(--primary);
            animation: spin 1s ease-in-out infinite;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        .hidden {
            display: none !important;
        }
        .status-message {
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            text-align: center;
            font-weight: 600;
        }
        .status-success {
            background: rgba(0, 255, 136, 0.1);
            border: 1px solid var(--success);
            color: var(--success);
        }
        .status-error {
            background: rgba(255, 68, 68, 0.1);
            border: 1px solid var(--error);
            color: var(--error);
        }
        .status-info {
            background: rgba(0, 255, 255, 0.1);
            border: 1px solid var(--accent);
            color: var(--accent);
        }
        /* Scrollbar Styling */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: var(--dark);
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(var(--primary), var(--secondary));
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(var(--secondary), var(--primary));
        }
        /* Mobile Responsive */
        @media (max-width: 768px) {
            .main-layout {
                grid-template-columns: 1fr;
                height: auto;
            }
            .sidebar {
                display: none;
            }
            .main-title {
                font-size: 2.5rem;
            }
            .control-bar {
                flex-direction: column;
                gap: 15px;
                padding: 15px;
            }
            .model-selector {
                flex-wrap: wrap;
                justify-content: center;
            }
            .image-controls {
                grid-template-columns: 1fr;
            }
            .preview-area {
                grid-template-columns: 1fr;
            }
            .tab-header {
                overflow-x: auto;
                padding: 0 15px;
            }
            .tab-btn {
                padding: 15px 20px;
                font-size: 1rem;
                white-space: nowrap;
            }
            .modal-content {
                margin: 10% auto;
                padding: 20px;
                width: 95%;
            }
            .chat-container {
                height: 400px;
                padding: 15px;
            }
            .message {
                max-width: 95%;
                padding: 15px;
            }
            .input-area {
                flex-direction: column;
                gap: 10px;
            }
            .send-btn {
                width: 100%;
                margin-top: 10px;
            }
            .image-results {
                grid-template-columns: 1fr;
            }
            .upload-zone {
                padding: 40px 20px;
            }
            .upload-icon {
                font-size: 3rem;
            }
            .upload-text {
                font-size: 1.1rem;
            }
            .modal-buttons {
                flex-direction: column;
            }
            .modal-btn {
                width: 100%;
            }
        }
        /* Small Mobile */
        @media (max-width: 480px) {
            .container {
                padding: 10px;
            }
            .header {
                padding: 20px 0;
            }
            .main-title {
                font-size: 2rem;
            }
            .subtitle {
                font-size: 1rem;
            }
            .control-group {
                padding: 15px;
            }
            .prompt-input {
                padding: 15px;
            }
            .generate-btn {
                padding: 15px 30px;
                font-size: 1rem;
            }
            .tab-btn {
                padding: 12px 15px;
                font-size: 0.9rem;
            }
            .message-input {
                padding: 15px;
            }
        }
        /* Cyber Elements */
        .cyber-line {
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--primary), transparent);
            margin: 20px 0;
            opacity: 0.5;
        }
        .pulse-glow {
            animation: pulseGlow 2s ease-in-out infinite alternate;
        }
        @keyframes pulseGlow {
            from { box-shadow: 0 0 20px var(--primary); }
            to { box-shadow: 0 0 30px var(--secondary), 0 0 40px var(--primary); }
        }
    </style>
</head>
<body data-theme="dark">
    <div class="cyber-grid"></div>
   
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1 class="main-title">⚡ NEXUS AI</h1>
            <p class="subtitle">ADVANCED AI ASSISTANT & CREATIVE STUDIO</p>
        </div>
        <!-- Control Bar -->
        <div class="control-bar">
            <button class="theme-toggle" onclick="toggleTheme()">
                <i class="fas fa-moon"></i>
                <span>THEME</span>
            </button>
           
            <div class="model-selector">
                <div class="model-btn active" data-model="gpt5">
                    <i class="fas fa-brain"></i>
                    GPT-5
                </div>
                <div class="model-btn" data-model="grok">
                    <i class="fas fa-robot"></i>
                    Grok
                </div>
                <div class="model-btn" data-model="qwen">
                    <i class="fas fa-star"></i>
                    Qwen
                </div>
                <div class="model-btn" data-model="deepseek">
                    <i class="fas fa-search"></i>
                    DeepSeek
                </div>
            </div>
        </div>
        <!-- Main Layout -->
        <div class="main-layout">
            <!-- Sidebar -->
            <div class="sidebar">
                <div class="sidebar-header">
                    <h3 class="sidebar-title">CHAT HISTORY</h3>
                    <button class="new-chat-btn" onclick="createNewChat()">
                        <i class="fas fa-plus"></i>
                        NEW
                    </button>
                </div>
                <div class="chat-list" id="chatList">
                    <!-- Chat items will be populated here -->
                </div>
            </div>
            <!-- Main Content -->
            <div class="main-content">
                <!-- Tab Header -->
                <div class="tab-header">
                    <button class="tab-btn active" data-tab="chat">
                        <i class="fas fa-comments"></i>
                        AI CHAT
                    </button>
                    <button class="tab-btn" data-tab="image">
                        <i class="fas fa-image"></i>
                        IMAGE GENERATOR
                    </button>
                    <button class="tab-btn" data-tab="bg-remover">
                        <i class="fas fa-cut"></i>
                        BG REMOVER
                    </button>
                </div>
                <!-- Chat Tab -->
                <div class="tab-content active" id="chat-tab">
                    <div class="chat-container" id="chatContainer">
                        <div class="message bot-message">
                            <div class="message-header">
                                <i class="fas fa-robot"></i>
                                NEXUS AI
                            </div>
                            Welcome to Nexus AI! I'm your advanced AI assistant. How can I help you today?
                        </div>
                    </div>
                   
                    <div class="input-area">
                        <textarea class="message-input" id="messageInput" placeholder="Type your message here..." rows="1"></textarea>
                        <button class="send-btn" onclick="sendMessage()" id="sendBtn">
                            <i class="fas fa-paper-plane"></i>
                            SEND
                        </button>
                    </div>
                </div>
                <!-- Image Generation Tab -->
                <div class="tab-content" id="image-tab">
                    <div class="image-controls">
                        <div class="control-group prompt-area">
                            <label class="control-label">
                                <i class="fas fa-pencil-alt"></i>
                                PROMPT
                            </label>
                            <textarea class="prompt-input" id="imagePrompt" placeholder="Describe the image you want to create... Be as detailed as possible for better results!"></textarea>
                        </div>
                       
                        <div class="control-group">
                            <label class="control-label">
                                <i class="fas fa-expand-alt"></i>
                                ASPECT RATIO
                            </label>
                            <select class="message-input" id="imageRatio">
                                <option value="1:1">1:1 Square</option>
                                <option value="16:9">16:9 Widescreen</option>
                                <option value="4:3">4:3 Standard</option>
                                <option value="3:4">3:4 Portrait</option>
                                <option value="19:6">19:6 Ultra Wide</option>
                            </select>
                        </div>
                       
                        <div class="control-group">
                            <label class="control-label">
                                <i class="fas fa-layer-group"></i>
                                IMAGE COUNT
                            </label>
                            <input type="number" class="message-input" id="imageCount" min="1" max="4" value="1">
                        </div>
                        <div class="control-group">
                            <label class="control-label">
                                <i class="fas fa-cogs"></i>
                                IMAGE MODEL
                            </label>
                            <select class="message-input" id="imageModel">
                                <option value="pollinations">Pollinations AI</option>
                                <option value="trax">Trax Dinosaur</option>
                                <option value="prexzy">Prexzy Imagen</option>
                            </select>
                        </div>
                    </div>
                   
                    <button class="generate-btn" onclick="generateImage()" id="generateBtn">
                        <i class="fas fa-magic"></i>
                        GENERATE IMAGES
                    </button>
                   
                    <div class="image-results" id="imageResults"></div>
                </div>
                <!-- BG Remover Tab -->
                <div class="tab-content" id="bg-remover-tab">
                    <div class="upload-zone" id="uploadZone" onclick="document.getElementById('fileInput').click()">
                        <div class="upload-icon">
                            <i class="fas fa-cloud-upload-alt"></i>
                        </div>
                        <div class="upload-text">UPLOAD IMAGE</div>
                        <div class="upload-subtext">Click to browse or drag & drop your image here</div>
                        <div class="upload-subtext">Supports: PNG, JPG, JPEG (Max 10MB)</div>
                        <input type="file" id="fileInput" class="file-input" accept="image/png, image/jpg, image/jpeg">
                    </div>
                    <div class="preview-area hidden" id="previewArea">
                        <div class="preview-card">
                            <div class="preview-title">ORIGINAL IMAGE</div>
                            <img class="preview-image" id="originalPreview" alt="Original Image">
                        </div>
                       
                        <div class="preview-card">
                            <div class="preview-title">BACKGROUND REMOVED</div>
                            <div id="processedPreview">
                                <div class="status-message status-info">
                                    <i class="fas fa-sync fa-spin"></i>
                                    Processing...
                                </div>
                            </div>
                        </div>
                    </div>
                    <button class="action-btn hidden" id="processBtn" onclick="processImage()">
                        <i class="fas fa-cut"></i>
                        REMOVE BACKGROUND
                    </button>
                    <button class="another-btn hidden" id="anotherBtn" onclick="uploadAnother()">
                        <i class="fas fa-plus"></i>
                        UPLOAD ANOTHER
                    </button>
                    <div id="bgResults"></div>
                </div>
            </div>
        </div>
    </div>
    <!-- Delete Modal -->
    <div id="deleteModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal('deleteModal')">&times;</span>
            <div class="modal-header">
                <i class="fas fa-exclamation-triangle"></i> Delete Chat
            </div>
            <div class="modal-body">
                Are you sure you want to delete this chat? This action cannot be undone.
            </div>
            <div class="modal-buttons">
                <button class="modal-btn modal-btn-secondary" onclick="closeModal('deleteModal')">Cancel</button>
                <button class="modal-btn modal-btn-primary" onclick="confirmDelete()" id="confirmDelete">Delete</button>
            </div>
        </div>
    </div>
    <!-- Rename Modal -->
    <div id="renameModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal('renameModal')">&times;</span>
            <div class="modal-header">
                <i class="fas fa-edit"></i> Rename Chat
            </div>
            <div class="modal-body">
                Enter a new name for this chat:
            </div>
            <input type="text" class="modal-input" id="renameInput" placeholder="Chat name">
            <div class="modal-buttons">
                <button class="modal-btn modal-btn-secondary" onclick="closeModal('renameModal')">Cancel</button>
                <button class="modal-btn modal-btn-primary" onclick="confirmRename()">Rename</button>
            </div>
        </div>
    </div>
    <script>
        // Global state
        let currentChatId = 'chat-' + Date.now();
        let chats = {};
        let currentTheme = 'dark';
        let currentModel = 'gpt5';
        let currentTab = 'chat';
        let loadingMessageId = null;
        let chatIdToDelete = null;

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            loadChatHistory();
            setupEventListeners();
            loadTheme();
            createNewChat();
        });

        function setupEventListeners() {
            // Tab switching
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    switchTab(this.dataset.tab);
                });
            });

            // Model selection
            document.querySelectorAll('.model-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    switchModel(this.dataset.model);
                });
            });

            // Message input auto-resize and enter to send
            const messageInput = document.getElementById('messageInput');
            messageInput.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = Math.min(this.scrollHeight, 120) + 'px';
            });
            messageInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            });

            // File upload handling
            const fileInput = document.getElementById('fileInput');
            const uploadZone = document.getElementById('uploadZone');
            fileInput.addEventListener('change', handleFileSelect);
           
            // Drag and drop
            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                uploadZone.addEventListener(eventName, preventDefaults, false);
            });

            function preventDefaults(e) {
                e.preventDefault();
                e.stopPropagation();
            }

            ['dragenter', 'dragover'].forEach(eventName => {
                uploadZone.addEventListener(eventName, () => {
                    uploadZone.classList.add('dragover');
                }, false);
            });

            ['dragleave', 'drop'].forEach(eventName => {
                uploadZone.addEventListener(eventName, () => {
                    uploadZone.classList.remove('dragover');
                }, false);
            });

            uploadZone.addEventListener('drop', handleDrop, false);
        }

        function handleFileSelect(e) {
            const file = e.target.files[0];
            if (file) processSelectedFile(file);
        }

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const file = dt.files[0];
            if (file) processSelectedFile(file);
        }

        function processSelectedFile(file) {
            if (!file.type.match('image.*')) {
                showStatus('Please select an image file (PNG, JPG, JPEG)', 'error');
                return;
            }
            if (file.size > 10 * 1024 * 1024) {
                showStatus('File size must be less than 10MB', 'error');
                return;
            }

            const reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById('originalPreview').src = e.target.result;
                document.getElementById('previewArea').classList.remove('hidden');
                document.getElementById('processBtn').classList.remove('hidden');
                document.getElementById('uploadZone').style.display = 'none';
            };
            reader.readAsDataURL(file);
        }

        function uploadAnother() {
            document.getElementById('fileInput').value = '';
            document.getElementById('previewArea').classList.add('hidden');
            document.getElementById('processBtn').classList.add('hidden');
            document.getElementById('anotherBtn').classList.add('hidden');
            document.getElementById('uploadZone').style.display = 'block';
            document.getElementById('processedPreview').innerHTML = '<div class="status-message status-info"><i class="fas fa-sync fa-spin"></i> Processing...</div>';
        }

        // Modal functions
        function showModal(modalId, chatId = null) {
            document.getElementById(modalId).style.display = 'block';
            if (modalId === 'renameModal' && chatId) {
                document.getElementById('renameInput').dataset.chatId = chatId;
                document.getElementById('renameInput').value = chats[chatId].name;
            } else if (modalId === 'deleteModal' && chatId) {
                chatIdToDelete = chatId;
            }
        }

        function closeModal(modalId) {
            document.getElementById(modalId).style.display = 'none';
        }

        function confirmRename() {
            const input = document.getElementById('renameInput');
            const chatId = input.dataset.chatId;
            const newName = input.value.trim() || 'New Chat';
            
            if (chats[chatId]) {
                chats[chatId].name = newName;
                saveChatHistory();
                loadChatHistory();
                closeModal('renameModal');
            }
        }

        function confirmDelete() {
            if (chatIdToDelete && chats[chatIdToDelete]) {
                delete chats[chatIdToDelete];
                saveChatHistory();
                loadChatHistory();
                
                if (currentChatId === chatIdToDelete) {
                    createNewChat();
                }
                
                closeModal('deleteModal');
                chatIdToDelete = null;
            }
        }

        // Close modals on outside click
        window.onclick = function(event) {
            const modals = document.querySelectorAll('.modal');
            modals.forEach(modal => {
                if (event.target === modal) {
                    modal.style.display = 'none';
                }
            });
        }

        // Theme management
        function toggleTheme() {
            currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.body.setAttribute('data-theme', currentTheme);
            localStorage.setItem('theme', currentTheme);
           
            const themeIcon = document.querySelector('.theme-toggle i');
            themeIcon.className = currentTheme === 'dark' ? 'fas fa-moon' : 'fas fa-sun';
        }

        function loadTheme() {
            const savedTheme = localStorage.getItem('theme') || 'dark';
            currentTheme = savedTheme;
            document.body.setAttribute('data-theme', currentTheme);
           
            const themeIcon = document.querySelector('.theme-toggle i');
            themeIcon.className = currentTheme === 'dark' ? 'fas fa-moon' : 'fas fa-sun';
        }

        // Tab management
        function switchTab(tabName) {
            currentTab = tabName;
           
            // Update tab buttons
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.tab === tabName);
            });
           
            // Update tab content
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.toggle('active', content.id === tabName + '-tab');
            });
        }

        // Model management
        function switchModel(modelName) {
            currentModel = modelName;
           
            // Update model buttons
            document.querySelectorAll('.model-btn').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.model === modelName);
            });
        }

        // Chat management
        function createNewChat() {
            currentChatId = 'chat-' + Date.now();
            chats[currentChatId] = {
                name: 'New Chat',
                messages: [
                    {
                        role: 'assistant',
                        content: "Welcome to Nexus AI! I'm your advanced AI assistant. How can I help you today?"
                    }
                ],
                createdAt: new Date().toISOString()
            };
           
            document.getElementById('chatContainer').innerHTML = `
                <div class="message bot-message">
                    <div class="message-header">
                        <i class="fas fa-robot"></i>
                        NEXUS AI
                    </div>
                    Welcome to Nexus AI! I'm your advanced AI assistant. How can I help you today?
                </div>
            `;
           
            saveChatHistory();
            loadChatHistory();
        }

        function loadChatHistory() {
            const savedChats = localStorage.getItem('nexusChats');
            if (savedChats) {
                chats = JSON.parse(savedChats);
            }
            
            const chatList = document.getElementById('chatList');
            chatList.innerHTML = '';
            
            // Sort chats by creation date (newest first)
            const sortedChatIds = Object.keys(chats).sort((a, b) => {
                return new Date(chats[b].createdAt) - new Date(chats[a].createdAt);
            });

            sortedChatIds.forEach(chatId => {
                const chat = chats[chatId];
                const lastMessage = chat.messages.length > 0 ?
                    chat.messages[chat.messages.length - 1].content : 'No messages yet';
               
                let displayName = chat.name;
                if (displayName === 'New Chat' && chat.messages.length > 1) {
                    const firstUserMessage = chat.messages.find(msg => msg.role === 'user');
                    if (firstUserMessage) {
                        displayName = firstUserMessage.content.substring(0, 30) +
                                    (firstUserMessage.content.length > 30 ? '...' : '');
                    }
                }
               
                const chatItem = document.createElement('div');
                chatItem.className = `chat-item ${chatId === currentChatId ? 'active' : ''}`;
                chatItem.dataset.chatId = chatId;
                chatItem.innerHTML = `
                    <div class="chat-content">
                        <div class="chat-name">${displayName}</div>
                        <div class="chat-preview">${lastMessage.substring(0, 50)}${lastMessage.length > 50 ? '...' : ''}</div>
                        <div class="chat-time">${formatTime(chat.createdAt)}</div>
                    </div>
                    <div class="chat-actions">
                        <button class="chat-action-btn" onclick="event.stopPropagation(); showModal('renameModal', '${chatId}')" title="Rename">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="chat-action-btn" onclick="event.stopPropagation(); showModal('deleteModal', '${chatId}')" title="Delete">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                `;
               
                chatItem.addEventListener('click', function(e) {
                    if (!e.target.closest('.chat-actions')) {
                        loadChat(chatId);
                    }
                });
                
                chatList.appendChild(chatItem);
            });
        }

        function loadChat(chatId) {
            currentChatId = chatId;
            const chat = chats[chatId];
           
            const chatContainer = document.getElementById('chatContainer');
            chatContainer.innerHTML = '';
           
            chat.messages.forEach(msg => {
                const messageDiv = document.createElement('div');
                messageDiv.className = msg.role === 'user' ? 'user-message message' : 'bot-message message';
                messageDiv.innerHTML = `
                    <div class="message-header">
                        <i class="fas ${msg.role === 'user' ? 'fa-user' : 'fa-robot'}"></i>
                        ${msg.role === 'user' ? 'YOU' : 'NEXUS AI'}
                    </div>
                    ${msg.content}
                `;
                chatContainer.appendChild(messageDiv);
            });
           
            chatContainer.scrollTop = chatContainer.scrollHeight;
            loadChatHistory();
        }

        function saveChatHistory() {
            localStorage.setItem('nexusChats', JSON.stringify(chats));
        }

        function formatTime(isoString) {
            const date = new Date(isoString);
            return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        }

        // Message sending
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
           
            if (!message) return;

            // Add user message
            addMessageToChat('user', message);
            input.value = '';
            input.style.height = 'auto';

            // Disable send button
            const sendBtn = document.getElementById('sendBtn');
            sendBtn.disabled = true;
            sendBtn.innerHTML = '<div class="loading"></div> PROCESSING';

            // Add loading message
            showLoadingMessage();

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        model: currentModel,
                        chatId: currentChatId
                    })
                });
                
                const data = await response.json();
                
                // Remove loading message
                hideLoadingMessage();
                
                if (data.success) {
                    addMessageToChat('assistant', data.response);
                } else {
                    addMessageToChat('assistant', 'Sorry, I encountered an error. Please try again.');
                }
            } catch (error) {
                // Remove loading message
                hideLoadingMessage();
                addMessageToChat('assistant', 'Network error. Please check your connection and try again.');
            } finally {
                // Re-enable send button
                sendBtn.disabled = false;
                sendBtn.innerHTML = '<i class="fas fa-paper-plane"></i> SEND';
            }
        }

        function showLoadingMessage() {
            const chatContainer = document.getElementById('chatContainer');
            const loadingDiv = document.createElement('div');
            loadingDiv.id = 'loadingMessage';
            loadingDiv.className = 'message bot-message loading-message';
            loadingDiv.innerHTML = `
                <div class="message-header">
                    <i class="fas fa-robot"></i>
                    NEXUS AI
                </div>
                <div><span class="loading-spinner"></span> Thinking...</div>
            `;
            chatContainer.appendChild(loadingDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
            loadingMessageId = 'loadingMessage';
        }

        function hideLoadingMessage() {
            const loadingDiv = document.getElementById('loadingMessage');
            if (loadingDiv) {
                loadingDiv.remove();
            }
        }

        function addMessageToChat(role, content) {
            if (!chats[currentChatId]) {
                createNewChat();
            }

            // Update chat name if it's the first user message
            if (role === 'user' && chats[currentChatId].name === 'New Chat') {
                chats[currentChatId].name = content.substring(0, 30) + (content.length > 30 ? '...' : '');
            }

            chats[currentChatId].messages.push({ role, content });
            saveChatHistory();

            const chatContainer = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            messageDiv.className = role === 'user' ? 'user-message message' : 'bot-message message';
            messageDiv.innerHTML = `
                <div class="message-header">
                    <i class="fas ${role === 'user' ? 'fa-user' : 'fa-robot'}"></i>
                    ${role === 'user' ? 'YOU' : 'NEXUS AI'}
                </div>
                ${content}
            `;
           
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
           
            loadChatHistory();
        }

        // Image generation
        async function generateImage() {
            const prompt = document.getElementById('imagePrompt').value.trim();
            const ratio = document.getElementById('imageRatio').value;
            const count = parseInt(document.getElementById('imageCount').value);
            const imageModel = document.getElementById('imageModel').value;

            if (!prompt) {
                showStatus('Please enter a prompt for image generation', 'error');
                return;
            }

            const generateBtn = document.getElementById('generateBtn');
            generateBtn.disabled = true;
            generateBtn.innerHTML = '<div class="loading"></div> GENERATING...';

            const resultsDiv = document.getElementById('imageResults');
            resultsDiv.innerHTML = '<div class="status-message status-info"><i class="fas fa-sync fa-spin"></i> Generating images... This may take a few moments.</div>';

            try {
                const response = await fetch('/api/generate-image', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        prompt: prompt,
                        ratio: ratio,
                        count: count,
                        model: imageModel
                    })
                });

                const data = await response.json();
                
                if (data.success) {
                    resultsDiv.innerHTML = '';
                    data.images.forEach((imageUrl, index) => {
                        const imageCard = document.createElement('div');
                        imageCard.className = 'image-card';
                        imageCard.innerHTML = `
                            <img src="${imageUrl}" class="image-preview" alt="Generated image ${index + 1}">
                            <div class="image-actions">
                                <button class="image-btn" onclick="downloadImage('${imageUrl}', 'nexus-image-${index + 1}.png')">
                                    <i class="fas fa-download"></i> DOWNLOAD
                                </button>
                                <button class="image-btn" onclick="viewImage('${imageUrl}')">
                                    <i class="fas fa-expand"></i> VIEW
                                </button>
                            </div>
                        `;
                        resultsDiv.appendChild(imageCard);
                    });
                } else {
                    resultsDiv.innerHTML = `<div class="status-message status-error">${data.error || 'Failed to generate images'}</div>`;
                }
            } catch (error) {
                resultsDiv.innerHTML = '<div class="status-message status-error">Network error. Please try again.</div>';
            } finally {
                generateBtn.disabled = false;
                generateBtn.innerHTML = '<i class="fas fa-magic"></i> GENERATE IMAGES';
            }
        }

        // Background removal
        async function processImage() {
            const fileInput = document.getElementById('fileInput');
            const file = fileInput.files[0];
            
            if (!file) {
                showStatus('Please select an image first', 'error');
                return;
            }

            const processBtn = document.getElementById('processBtn');
            processBtn.disabled = true;
            processBtn.innerHTML = '<div class="loading"></div> PROCESSING...';

            const processedPreview = document.getElementById('processedPreview');
            processedPreview.innerHTML = '<div class="status-message status-info"><i class="fas fa-sync fa-spin"></i> Removing background... This may take a few seconds.</div>';

            const formData = new FormData();
            formData.append('image', file);

            try {
                const response = await fetch('/api/remove-bg', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();
                
                if (data.success) {
                    processedPreview.innerHTML = `
                        <img src="${data.imageUrl}" class="preview-image" alt="Background removed">
                        <div class="image-actions" style="margin-top: 15px;">
                            <button class="image-btn" onclick="downloadImage('${data.imageUrl}', 'nexus-bg-removed.png')">
                                <i class="fas fa-download"></i> DOWNLOAD
                            </button>
                        </div>
                    `;
                    document.getElementById('anotherBtn').classList.remove('hidden');
                } else {
                    processedPreview.innerHTML = `<div class="status-message status-error">${data.error || 'Failed to remove background'}</div>`;
                }
            } catch (error) {
                processedPreview.innerHTML = '<div class="status-message status-error">Network error. Please try again.</div>';
            } finally {
                processBtn.disabled = false;
                processBtn.innerHTML = '<i class="fas fa-cut"></i> REMOVE BACKGROUND';
            }
        }

        // Utility functions
        function showStatus(message, type) {
            const statusDiv = document.createElement('div');
            statusDiv.className = `status-message status-${type}`;
            statusDiv.textContent = message;
           
            document.getElementById(currentTab + '-tab').insertBefore(statusDiv, document.getElementById(currentTab + '-tab').firstChild);
           
            setTimeout(() => {
                statusDiv.remove();
            }, 5000);
        }

        function downloadImage(url, filename) {
            const link = document.createElement('a');
            link.href = url;
            link.download = filename;
            link.click();
        }

        function viewImage(url) {
            window.open(url, '_blank');
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/chat', methods=['POST'])
def api_chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        model = data.get('model', 'gpt5')
        chat_id = data.get('chatId', '')

        if not message:
            return jsonify({'success': False, 'error': 'No message provided'})

        # Prepare the conversation history
        messages = [{"role": "user", "content": message}]

        # Route to appropriate API based on model selection
        if model == 'gpt5':
            response = handle_gpt5(messages)
        elif model == 'grok':
            response = handle_grok(messages)
        elif model == 'qwen':
            response = handle_qwen(messages)
        elif model == 'deepseek':
            response = handle_deepseek(messages)
        else:
            response = handle_gpt5(messages) # Default fallback

        return jsonify({'success': True, 'response': response})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def handle_gpt5(messages):
    try:
        text = messages[-1]['content']
        system_prompt = 'You are a helpful AI assistant that provides accurate, concise, and context-aware responses.'
       
        api_url = f"{GPT5_API_URL}?text={quote(text)}&systemPrompt={quote(system_prompt)}"
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
       
        data = response.json()
        return data.get('result', 'No response from GPT-5 API')
   
    except Exception as e:
        return f"GPT-5 Error: {str(e)}"

def handle_grok(messages):
    try:
        response = requests.post(
            url=OPENROUTER_BASE_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY_GROK}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "x-ai/grok-4-fast:free",
                "messages": messages
            }),
            timeout=30
        )
        response.raise_for_status()
       
        data = response.json()
        return data['choices'][0]['message']['content']
   
    except Exception as e:
        return f"Grok Error: {str(e)}"

def handle_qwen(messages):
    try:
        response = requests.post(
            url=OPENROUTER_BASE_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY_QWEN}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "qwen/qwen3-4b:free",
                "messages": messages
            }),
            timeout=30
        )
        response.raise_for_status()
       
        data = response.json()
        return data['choices'][0]['message']['content']
   
    except Exception as e:
        return f"Qwen Error: {str(e)}"

def handle_deepseek(messages):
    try:
        response = requests.post(
            url=SAMBANOVA_API_URL,
            headers={
                "Authorization": f"Bearer {SAMBANOVA_API_KEY}",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": "DeepSeek-R1-0528",
                "messages": messages,
                "stream": False
            }),
            timeout=30
        )
        response.raise_for_status()
       
        data = response.json()
        return data['choices'][0]['message']['content']
   
    except Exception as e:
        return f"DeepSeek Error: {str(e)}"

@app.route('/api/generate-image', methods=['POST'])
def api_generate_image():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        ratio = data.get('ratio', '1:1')
        count = data.get('count', 1)
        model = data.get('model', 'pollinations')

        if not prompt:
            return jsonify({'success': False, 'error': 'No prompt provided'})

        ratio_map = {
            '1:1': {'width': 1024, 'height': 1024},
            '16:9': {'width': 1280, 'height': 720},
            '4:3': {'width': 1024, 'height': 768},
            '3:4': {'width': 768, 'height': 1024},
            '19:6': {'width': 1900, 'height': 600}
        }

        dimensions = ratio_map.get(ratio, ratio_map['1:1'])
        image_urls = []

        for i in range(min(count, 4)): # Max 4 images
            try:
                if model == 'pollinations':
                    api_url = f"{POLL_IMAGE_URL}/{quote(prompt)}?width={dimensions['width']}&height={dimensions['height']}&nologo=true&seed={i+1}"
                    response = requests.get(api_url, timeout=60)
                    response.raise_for_status()
                    image_urls.append(response.url)
                elif model == 'prexzy':
                    api_url = f"{PREXZY_IMAGE_URL}?prompt={quote(prompt)}&ratio={quote(ratio)}"
                    response = requests.get(api_url, timeout=60)
                    response.raise_for_status()
                    image_urls.append(response.url)
                else: # trax
                    trax_response = requests.post(
                        TRAXDINOSAUR_API_URL,
                        headers={"Content-Type": "application/json"},
                        json={"prompt": prompt},
                        timeout=60
                    )
                    if trax_response.status_code == 200:
                        img_base64 = b64encode(trax_response.content).decode('utf-8')
                        image_urls.append(f"data:image/png;base64,{img_base64}")
            except Exception as e:
                continue

        return jsonify({'success': True, 'images': image_urls})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/remove-bg', methods=['POST'])
def api_remove_bg():
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image file provided'})

        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No image file selected'})

        files = {'image': (file.filename, file.read(), file.content_type)}
        response = requests.post(
            TRAXBG_API_URL,
            files=files,
            headers={"Accept": "application/json"},
            timeout=60
        )
        response.raise_for_status()
        data = response.json()

        if data.get('status') == 'success' and data.get('output_url'):
            return jsonify({
                'success': True,
                'imageUrl': data['output_url']
            })
        else:
            return jsonify({'success': False, 'error': 'Background removal failed'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


