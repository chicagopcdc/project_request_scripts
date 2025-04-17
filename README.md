# project_request_scripts
This repo contains the scripts used to prepare the data for approved project request

1. TODO - call pelican API endpoint with the correct credentials and the correct filter.
2. TODO - filter the required columns by consortiums
3. Generate the ZIP file with the data for the approved project request
4. TODO - upload the generated ZIP on S3
5. Call the Amanuensis API endpoint to update the project approved_url

Point 1 could be part of amanuensis or a job triggered by amanuensis on request state change to `Approved`.
