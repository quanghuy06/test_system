/**
* TSDV - PHOcr team
* Author: Tai Phung Dinh
* Date created: 30/09/2019
* Description: This script defines some groovy functions to help handling json file more convenient
*/
import groovy.json.JsonSlurper
import groovy.json.JsonOutput

/**
* Read a json file to object
*/
def LoadJson(String file_path) {
    // Create file object
    File json_file = new File(file_path)

    // If file does not exist then return null object
    if (!json_file.exists()) {
        // Warning to user
        println("WARN: LoadJson: No such file ${file_path}")
        return null
    }

    // Parse json object
    def jsonSlurper = new JsonSlurper()
    def jsonObject = jsonSlurper.parse(json_file)

    // Return status of voting execution
    return jsonObject
}

/**
* Write a json object to file
*/
def WriteJson(Object json_object, String file_path) {
    // Create file object
    File file = new File(file_path)

    // Producing json string
    def json_str = JsonOutput.toJson(json_object)

    // Format json string output
    def json_beauty = JsonOutput.prettyPrint(json_str)

    // Write json string to output file
    file.write(json_beauty)
}

return this
