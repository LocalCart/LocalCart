var Action = (function() {

   // var apiUrl = 'https://smileback-cs169.herokuapp.com';

    var submitRegistration;
    var search;

    /**
     * HTTP GET request
     * @param  {string}   url       URL path, e.g. "/api/smiles"
     * @param  {function} onSuccess   callback method to execute upon request success (200 status)
     * @param  {function} onFailure   callback method to execute upon request failure (non-200 status)
     * @return {None}
     */
    var makeGetRequest = function(url, onSuccess, onFailure) {
        $.ajax({
            type: 'GET',
            url: apiUrl + url,
            dataType: "json",
            success: onSuccess,
            error: onFailure
        });
    };

    /**
     * HTTP POST request
     * @param  {string}   url       URL path, e.g. "/api/smiles"
     * @param  {Object}   data      JSON data to send in request body
     * @param  {function} onSuccess   callback method to execute upon request success (200 status)
     * @param  {function} onFailure   callback method to execute upon request failure (non-200 status)
     * @return {None}
     */
    var makePostRequest = function(url, data, onSuccess, onFailure) {
        $.ajax({
            type: 'POST',
            url: apiUrl + url,
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
            success: onSuccess,
            error: onFailure
        });
    };

    /**
     * Add event handlers for submitting the registration form.
     * @return {None}
     */
    var attachSubmitRegistrationHandler = function(e) {
        submitRegistration.on("click", ".my-button:first", function (e) {
            e.preventDefault();

            var submitRegistrationButton = $(this);
            var onSuccess = function (data) {
                if (data.status == -1) {
                    onFailure(data);
                    return;
                }

                window.location.replace(index.html);
            };
            var onFailure = function (data) {
                console.error('registration submission error');
                if (data.errors != undefined) {
                    for (var i = 0; i < data.errors.length; i++) {
                        console.error(data.errors[i]);
                    }
                }
            };

            makePostRequest(userType, username, email, password, onSuccess, onFailure);
        });
    }

     /**
     * Add event handlers for searching.
     * @return {None}
     */
    var attachSearchHandler = function(e) {
        search.on("click", ".my-button:first", function (e) {
            e.preventDefault();

            var searchButton = $(this);
            var onSuccess = function (data) {
                if (data.status == -1) {
                    onFailure(data);
                    return;
                }

                window.location.replace(search-results.html);
            };
            var onFailure = function (data) {
                console.error('search error');
                if (data.errors != undefined) {
                    for (var i = 0; i < data.errors.length; i++) {
                        console.error(data.errors[i]);
                    }
                }
            };

            makeGetRequest(query, undefined, 10, onSuccess, onFailure);
        });
    }


    /**
     * Start the app by displaying the most recent smiles and attaching event handlers.
     * @return {None}
     */
    var start = function() {
        submitRegistration = $(".submit-registration");
        search = $(".search-input");

        attachSubmitRegistrationHandler();
        attachSearchHandler();
    };
})();