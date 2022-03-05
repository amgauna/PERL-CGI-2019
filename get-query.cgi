#include  <stdio.h>
#include  <stdlib.h>

int main()
{
   char *query;
   
   printf("Content-type: text/plain\n\n");
   /* METHOD="GET" */
   query=getenv("QUERY_STRING");
   printf("Os dados recebidos do formulário são:\n\n");
   printf("%s\n", query);

   return(0);
}
