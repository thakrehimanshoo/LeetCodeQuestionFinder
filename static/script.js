$(document).ready(function() {
    var currentPage = 1; 
    $('#search-form').submit(function(e) {
        e.preventDefault(); 
        
        var query = $('#search-bar').val();
        
        $.ajax({
            type: 'POST',
            url: '/search',
            data: {query: query},
            success: function(response) {
                displayLinks(response.links, currentPage); 
            }
        });
    });
});

function displayLinks(links, currentPage) {
    var resultsContainer = $('#results');
    resultsContainer.empty();

    if (links.length === 0) {
        var noResultsHeading = $('<h1 class="no-results-heading">No results found.</h1>');
        resultsContainer.append(noResultsHeading);
    }
    else {
        var flexContainer = $('<div class="flex-container"></div>'); 
        resultsContainer.append(flexContainer);

        var startIndex = (currentPage - 1) * 6; 
        var endIndex = startIndex + 6; 

        var count = 0;

        $.each(links, function(index, link) {
            if (count >= startIndex && count < endIndex) {
                var title = link[0];
                var url = link[1];

                var card = $('<div class="card"></div>'); 

                var header = $('<div class="header"></div>');
                var span = $('<span class="title">' + title + '</span>'); 

                var button = $('<button type="button" class="action">Solve this</button>');
                button.click(function() {
                    window.open(url, '_blank'); 
                });

                header.append(span);
                card.append(header, button);
                flexContainer.append(card);
            }

            count++;
        });

       
        var totalPages = Math.ceil(links.length / 6); 
        if (totalPages > 1) {
            var pagination = $('<div class="pagination"></div>');
            
            
            if (currentPage > 1) {
                var prevButton = $('<button type="button" class="prev-button">Previous</button>');
                prevButton.click(function() {
                    displayLinks(links, currentPage - 1); 
                });
                pagination.append(prevButton);
            }
            
           
            if (currentPage < totalPages) {
                var nextButton = $('<button type="button" class="next-button">Next</button>');
                nextButton.click(function() {
                    displayLinks(links, currentPage + 1); 
                });
                pagination.append(nextButton);
            }
            
            resultsContainer.append(pagination);
        }
    }
}
