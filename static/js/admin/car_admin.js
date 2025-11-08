// Admin JavaScript for Car model
document.addEventListener('DOMContentLoaded', function() {
    // Add any dynamic behavior here
    
    // Example: Auto-format JSON fields
    const jsonFields = document.querySelectorAll('textarea[name$="station_fields"], textarea[name$="metadata"], textarea[name$="tags"], textarea[name$="notes"], textarea[name$="messages"], textarea[name$="custom_car_info"]');
    
    jsonFields.forEach(field => {
        field.addEventListener('change', function() {
            try {
                const value = JSON.parse(field.value);
                field.value = JSON.stringify(value, null, 2);
            } catch (e) {
                // Invalid JSON - leave as is
            }
        });
    });
});