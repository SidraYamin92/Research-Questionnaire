<?php
/**
 * Questionnaire Data Collection Endpoint
 * Receives and stores questionnaire responses
 */

// Enable error reporting for debugging (disable in production)
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Set headers
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Only allow POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
    exit();
}

// Get JSON data
$input = file_get_contents('php://input');
$data = json_decode($input, true);

// Validate data
if (!$data || !isset($data['responses']) || !isset($data['metadata'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid data format']);
    exit();
}

// Add server-side metadata
$data['server_metadata'] = [
    'received_at' => date('Y-m-d H:i:s'),
    'ip_address' => $_SERVER['REMOTE_ADDR'] ?? 'unknown',
    'server_time' => time()
];

// Generate unique participant ID
$participant_id = 'P_' . date('Ymd') . '_' . uniqid();
$data['participant_id'] = $participant_id;

// Create data directory if it doesn't exist
$data_dir = __DIR__ . '/data';
if (!file_exists($data_dir)) {
    mkdir($data_dir, 0755, true);
}

// Save to JSON file
$filename = $data_dir . '/response_' . $participant_id . '.json';
$save_result = file_put_contents($filename, json_encode($data, JSON_PRETTY_PRINT));

if ($save_result === false) {
    http_response_code(500);
    echo json_encode(['error' => 'Failed to save data']);
    exit();
}

// Optional: Save to CSV for easy analysis
saveToCsv($data, $data_dir . '/responses.csv');

// Optional: Send email notification
// sendEmailNotification($participant_id, $data);

// Success response
http_response_code(200);
echo json_encode([
    'success' => true,
    'message' => 'Data saved successfully',
    'participant_id' => $participant_id
]);

/**
 * Save response to CSV file
 */
function saveToCsv($data, $csv_file) {
    $is_new_file = !file_exists($csv_file);
    $fp = fopen($csv_file, 'a');
    
    if (!$fp) return false;
    
    // Flatten data for CSV
    $row = [
        'participant_id' => $data['participant_id'],
        'completion_date' => $data['metadata']['completionDate'] ?? '',
        'total_time' => $data['metadata']['totalTime'] ?? '',
        'user_agent' => $data['metadata']['userAgent'] ?? '',
        'screen_resolution' => $data['metadata']['screenResolution'] ?? ''
    ];
    
    // Add all responses
    if (isset($data['responses'])) {
        foreach ($data['responses'] as $key => $value) {
            if (is_array($value)) {
                $row[$key] = json_encode($value);
            } else {
                $row[$key] = $value;
            }
        }
    }
    
    // Add scenario conditions
    if (isset($data['metadata']['scenarioConditions'])) {
        foreach ($data['metadata']['scenarioConditions'] as $key => $value) {
            $row['condition_' . $key] = $value;
        }
    }
    
    // Write header if new file
    if ($is_new_file) {
        fputcsv($fp, array_keys($row));
    }
    
    // Write data
    fputcsv($fp, $row);
    fclose($fp);
    
    return true;
}

/**
 * Send email notification (optional)
 */
function sendEmailNotification($participant_id, $data) {
    $to = '[your-email@example.com]'; // Replace with your email
    $subject = 'New Questionnaire Response: ' . $participant_id;
    
    $message = "New questionnaire response received:\n\n";
    $message .= "Participant ID: " . $participant_id . "\n";
    $message .= "Completion Time: " . ($data['metadata']['totalTime'] ?? 'N/A') . " seconds\n";
    $message .= "Date: " . ($data['metadata']['completionDate'] ?? 'N/A') . "\n";
    $message .= "\nTotal Responses: " . count($data['responses'] ?? []) . "\n";
    
    $headers = 'From: noreply@yourdomain.com' . "\r\n";
    
    // Uncomment to enable email notifications
    // mail($to, $subject, $message, $headers);
}
?>
