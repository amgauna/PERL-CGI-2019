#include  <stdio.h>
#include  <stdlib.h>

int main()
{
   char *query;
   int  length;
   
   printf("Content-type: text/plain\n\n");
   /* METHOD="POST" */
   length=atoi(getenv("CONTENT_LENGTH"));
   query=(char *) malloc(sizeof(char)*(length+1));
   if (query!=NULL)
      fread(query, length, sizeof(char), stdin);
   printf("Os dados recebidos do formulário são:\n\n");
   printf("%s\n\n", query);
   printf("A variável de ambiente CONTENT_LENGTH tem o valor %d.\n", length);

   return(0);
}
