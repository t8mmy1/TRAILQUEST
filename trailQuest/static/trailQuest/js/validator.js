/*
    Contains reusable input validation functions and form-specific handlers
    Used across all forms in Trail Quest
 */

/*
    Reusable Functions
 */
function isAlphanumericSpaceHyphen(input) {
    const pattern = /^[a-zA-Z0-9\s-]+$/;
    return pattern.test(input.value); 
}

function isAlphaNumSpacePeriodCommaHyphen(input) {
    const pattern = /^[a-zA-Z0-9\s-,.]+$/;
    return pattern.test(input.value); 
}

function isStrongPassword(input){
    const password = input.value;
    const messages = [];

    if (password.length < 8) {
        messages.push("Minimum 8 characters.");
    }
    if (!/[a-z]/.test(password)) {
        messages.push("At least one lowercase letter.");
    }
    if (!/[A-Z]/.test(password)) {
        messages.push("At least one uppercase letter.");
    }
    if (!/[0-9]/.test(password)) {
        messages.push("At least one number.");
    }
    if (!/[!@#$%^&*()_+={}.,?-]/.test(password)) {
        messages.push("At least one special character (!@#$%^&* etc.).");
    }

    if (messages.length > 0) {
        showError(input, "<ul><li>" + messages.join("</li><li>") + "</li></ul>");
        return false;
    } else {
        clearError(input);
        return true;
    }
}

function passwordsMatch(password, confirmPassword){
    if(password.value === confirmPassword.value){
        return true;
    }
    else{
        return false;
    }
}

function checkPasswordMatch(confirmPassword){ // FOR USER REGISTRATION FORM 
    const password = document.querySelector("#password");
    return passwordsMatch(password, confirmPassword);
}

function isInteger(input){

    const pattern = /^\d+$/;
    return pattern.test(input.value);

}

function isPositiveInteger(input){

    const pattern = /^-/;

    if(isInteger(input)){
        return !(pattern.test(input.value));
    }
    
    return false;

}

function isDecimal(input){
    const pattern = /^\d+\.\d+$/;
    return pattern.test(input.value);
}

function isPositiveDecimal(input){
    const pattern = /^-?$/;

    if(isDecimal(input)){
        return !(pattern.test(input.value));
    }
    
    return false;
}

function isNonEmpty(input){
    return input.value.length !== 0;
}

function isValidEmail(email){
    const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
    return pattern.test(email.value);
}

function isValidLat(input){

    if(isInteger(input) || isDecimal(input)){
        if (input.value >= -90 && input.value <= 90){
            return true;
        }
    }

    return false;
}

function isValidLong(input){

    if(isInteger(input) || isDecimal(input)){
        if (input.value >= -180 && input.value <= 180){
            return true;
        }
    }

    return false;
}

function showError(inputElement, message) {
    const errorElement = document.getElementById(inputElement.id + "Error");
    if (errorElement) {
        errorElement.innerHTML = message;
        inputElement.style.borderColor = "red";
    }
}

function clearError(inputElement) {
    const errorElement = document.getElementById(inputElement.id + "Error");
    if (errorElement) {
        errorElement.textContent = "";
        inputElement.style.borderColor = "#333";
    }
}

/*
    VALIDATION FOR EACH FORM USING REUSABLE FUNCTIONS ABOVE
*/

function validateTrailName(input){
    if (!isNonEmpty(input)) {
        showError(input, "Please enter trail name.");
    }
    else {
        clearError(input);
            if (!isAlphanumericSpaceHyphen(input)) {
                showError(input, "Trail Name can only contain letters, numbers, spaces, and hyphens.");
            }
            else{
                clearError(input);
            }
    }
}

function validateLocation(input){
    if (!isNonEmpty(input)) {
        showError(input, "Please enter location name.");
    }
    else {
        clearError(input);
            if (!isAlphanumericSpaceHyphen(input)) {
                showError(input, "Location name can only contain letters, numbers, spaces, and hyphens.");
            }
            else{
                clearError(input);
            }
    }
}

function validateDistance(input){
    if (!isNonEmpty(input)) {
        showError(input, "Please enter a distance in kms.");
    }
    else {
        clearError(input);
            if(!isValidPositiveNumber(input)){
                showError(input, "Please enter a valid positive number with a decimal place of 2.");
            }
            else{
                clearError(input);
            }
    }
}

function validateElevation(input){
    if (!isNonEmpty(input)) {
        showError(input, "Please enter an elevation in meters.");
    }
    else {
        clearError(input);
            if(!isValidPositiveNumber(input)){
                showError(input, "Please enter a valid positive number");
            }
            else{
                clearError(input);
            }
    }
}

function validateTime(input){
    if (!isNonEmpty(input)) {
        showError(input, "Please enter a time estimate.");
    }
    else {
        clearError(input);
            if(!isValidPositiveNumber(input)){
                showError(input, "Please enter a valid positive number with a decimal place of 2.");
            }
            else{
                clearError(input);
            }
    }
}

function validateOption(input){
    if (!isNonEmpty(input)) {
        showError(input, "Please choose an option.");
    }
    else{
        clearError(input);
    }
}


function validateUsername(input) {
    if (!isNonEmpty(input)) {
        showError(input, "Please enter your username.");
    }
    else {
        clearError(input);
    }
}

function validateEmail(input) {
    if (!isNonEmpty(input)) {
        showError(input, "Please enter your email address.");
    }
    else {
        clearError(input);
        if(!isValidEmail(input)){
            showError(input, "Please enter a valid email address.");
        }
        else{
            clearError(input);
        }
    }
}

function validatePassword(input) {
    if (!isNonEmpty(input)) {
        showError(input, "Please enter your password.");
    }
    else {
        clearError(input);
        isStrongPassword(input);
    }
}

function validateLoginPassword(input) {
    if (!isNonEmpty(input)) {
        showError(input, "Please enter your password.");
    }
    else {
        clearError(input);
    }
}

function confirmPasswordReg(input) {
    if (!isNonEmpty(input)) {
        showError(input, "Please confirm your password.");
    }
    else {
        clearError(input);
        checkPasswordMatch(input);
    }
}

function validateLogin(form){
    var valid = true;
    
    const username = form.username;
    const password = form.password;

    if (!isNonEmpty(username)) {
        valid = false;
        showError(username, "Please enter your username.");
    }
    else {
        clearError(username);
    }

    if (!isNonEmpty(password)) {
        valid = false;
        showError(password, "Please enter your password.");
    }
    else {
        clearError(password);
    }

    return valid;
}

function validateReviewTrail(form) {
    var valid = true;

    const rating = form.rating;

    if (!isNonEmpty(rating)) {
        valid = false;
        showError(rating, "Please select a rating.");
    } else {
        clearError(rating);
    }

    return valid;
}

function validateApproveTrail(form) {
    var valid = true;

    const approvalStatus = form.approvalStatus;
    const adminComments = form.adminComments;

    if (!isNonEmpty(approvalStatus)) {
        valid = false;
        showError(approvalStatus, "Please select an approval status.")
    } else {
        clearError(approvalStatus);
    }

    if (isNonEmpty(adminComments) && !isAlphaNumSpacePeriodCommaHyphen(adminComments)) {
        valid = false;
        showError(adminComments, "Comments can only include letters, numbers, spaces, periods, commas, and hyphens.")
    } else {
        clearError(adminComments);
    }

    return valid;
}

function isValidPositiveNumber(input) {
    const value = input.value;

    // Match integers and decimals greater than 0 (but not negative or zero)
    // const pattern = /^(?:[1-9]\d*|0?\.\d*[1-9]\d*)$/;
    const pattern = /^[+-]?\d{1,18}(\.\d{1,2})?$/;
     

    return pattern.test(value);
}


function validateTrailSubmission(form){
    var valid = true;

    // REQUIRED INPUTS 

    const name = form.trailName;
    const location = form.location;
    const distance = form.distance;
    const elevation = form.elevationGain;
    const difficulty = form.difficultyLevel;
    const type = form.trailType;
    const time = form.estimatedTime

    // IF N0N-REQUIRED INPUTS ARE USED, VALIDATE THEM
    const latitude = form.latitude;
    const longitude = form.longitude;
    const startPoint = form.startPoint;
    const endPoint = form.endPoint;
    const condition = form.trailConditions;
    const accessibility = form.accessibility;
    const userNotes = form.userNotes;



    if(!isNonEmpty(name)) {
        valid = false;
        showError(name, "Please enter a trail name.");
    }
    else {
        clearError(name);
    }

    if(!isNonEmpty(location)) {
        valid = false;
        showError(location, "Please enter a location.");
    }
    else {
        clearError(location);
    }



    if (!isValidPositiveNumber(distance)) {
    valid = false;
        showError(distance, "Please enter a positive number.");
    } else {
        clearError(distance);
    }


    if (!isValidPositiveNumber(elevation)) {
        valid = false;
        showError(elevation, "Please enter a positive number.");
    } else {
        clearError(elevation);
    }



    
    if(!isNonEmpty(difficulty)) {
        valid = false;
        showError(difficulty, "Please select a difficulty level.");
    }
    else{
        clearError(difficulty);
    }

    if(!isNonEmpty(type)) {
        valid = false;
        showError(type, "Please select a trail type.");
    }
    else{
        clearError(type);
    }



    if (!(isInteger(time))) { // IF NOT INTEGER

        if (isDecimal(time)) { // IF DECIMAL NUMBER
            
            if (!isPositiveDecimal(time)) { // IF IT'S NEGATIVE DECIMAL

                valid = false;
                showError(time, "Please enter valid elevation.");

            } 
            else { // IF POSITIVE DECIMAL

                clearError(time);

            }

        } 
        else { // IF NOT DECIMAL EITHER (INVALID INPUT)

            valid = false;
            showError(time, "Please enter a number.");

        }
    } 
    else { // IF INTEGER
        if (!isPositiveInteger(time)) { // IF NEGATIVE INTEGER

            valid = false;
            showError(time, "Please enter valid distance.");

        } else { // IF POSITIVE INTEGER

            clearError(time);

        }
    }

    // OPTIONAL INPUTS

    if(isNonEmpty(latitude)) {
        if (!isValidLat(latitude)) {
            valid = false;
            showError(latitude, "Please enter a valid latitude.");
        }
        else {
            clearError(latitude);
        }
    }

    if(isNonEmpty(longitude)) {
        if (!isValidLong(longitude)) {
            valid = false;
            showError(longitude, "Please enter a valid longitude.");
        }
        else {
            clearError(longitude);
        }
    }

    if(isNonEmpty(startPoint)) {
        if (!isAlphanumericSpaceHyphen(startPoint)) {
            valid = false;
            showError(startPoint, "Start point can only contain letters, numbers, spaces, and hyphens.");
        } else {
            clearError(startPoint);
        }
    }

    if(isNonEmpty(endPoint)) {
        if (!isAlphanumericSpaceHyphen(endPoint)) {
            valid = false;
            showError(endPoint, "End point can only contain letters, numbers, spaces, and hyphens.");
        } else {
            clearError(endPoint);
        }
    }

    if(isNonEmpty(condition)) {
        if (!isAlphanumericSpaceHyphen(condition)) {
            valid = false;
            showError(condition, "Trail conditions can only contain letters, numbers, spaces, and hyphens.");
        } else {
            clearError(condition);
        }
    }

    if(isNonEmpty(accessibility)) {
        if (!isAlphanumericSpaceHyphen(accessibility)) {
            valid = false;
            showError(accessibility, "Accessibility can only contain letters, numbers, spaces, and hyphens.");
        } else {
            clearError(accessibility);
        }
    }

    if(isNonEmpty(userNotes)) {
        if (!isAlphaNumSpacePeriodCommaHyphen(userNotes)) {
            valid = false;
            showError(userNotes, "Notes can only contain letters, numbers, spaces, periods, commas, and hyphens.");
        } else {
            clearError(userNotes);
        }
    }

    return valid;
}

function validateSearchTrail(form) {
    var valid = true;

    const trailName = form.trailName;
    const location = form.location;
    const min = form.minDist;
    const max = form.maxDist;
    const type = form.trailType;
    const difficulty = form.difficultyLevel;

    if (isNonEmpty(trailName)) {
        if (!isAlphanumericSpaceHyphen(trailName)) {
            valid = false;
            showError(trailName, "Trail name can only contain letters, numbers, spaces, and hyphens.");
        } else {
            clearError(trailName);
        }
    }

    if (isNonEmpty(location)) {
        if (!isAlphanumericSpaceHyphen(location)) {
            valid = false;
            showError(location, "Location can only contain letters, numbers, spaces, and hyphens.");
        } else {
            clearError(location);
        }
    }


    if (isNonEmpty(min)) {
        if (!isPositiveDecimal(min) && !isPositiveInteger(min)) {  // Check for both decimals and integers
            valid = false;
            showError(min, "Distance range must be a positive number.");
        } else {
            clearError(min);
        }
    }

    if (isNonEmpty(max)) {
        if (!isPositiveDecimal(max) && !isPositiveInteger(max)) {  // Check for both decimals and integers
            valid = false;
            showError(max, "Distance range must be a positive number.");
        } else {
            clearError(max);
        }
    }



    return valid;
}

function validateRegister(form) {
    var valid = true;

    const email = form.email;
    const username = form.username;
    const password = form.password;
    const confirmPassword = form.confirmPassword;

    if (!isValidEmail(email)) {
        valid = false;
        showError(email, "Please enter a valid email address.");
    } else {
        clearError(email);
    }

    if(!isAlphanumericSpaceHyphen(username)) {
        valid = false;
        showError(username, "Username can only contain letters, numbers, spaces, and hyphens.");
    }
    else {
        clearError(username);
    }

    // &1Ad1Ad%
    if (!isStrongPassword(password)) {
        valid = false;
    }

    if (!checkPasswordMatch(confirmPassword)) {
        valid = false;
        showError(confirmPassword, "Passwords do not match.");
    } else {
        clearError(confirmPassword);
    }

    return valid;
}

function validateCoordinate(input){
    const pattern = /^[+-]?\d+(\.\d{1,6})?$/;

    if (isNonEmpty(input)) {
        if(pattern.test(input.value) == false){
            showError(input, "Must be a valid coordinate with 6 decimal places");
        }
        else{
            clearError(input);
        }
    }
}