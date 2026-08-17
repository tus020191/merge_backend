from rest_framework.pagination import PageNumberPagination


class PostPagination(PageNumberPagination):

    #  this means per page 5 posts 
    page_size = 2

    #  this means we can use qry as page=2 for 2nd page so on
    page_query_param = "page"

    #  this means we can give our custome no of posts per page
    #  like this page_size=10 now this means per page 10 post
    page_size_query_param = "page_size"

    #  max page size we can customize is 20 
    max_page_size = 20

