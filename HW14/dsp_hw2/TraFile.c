#include<stdio.h>
#include<stdlib.h>
#include<string.h>
FILE *fp1,*fp2;



void main(void)
{
	char filename1[80],filename2[80];
	char tempstr[512];
    char text1[80];
	char text2[80];	
	double temp;
	int insideconter=1;
	fp1=fopen("output.txt","r");
	fp2=fopen("libsvmfile.txt","w");

	if(fp1 == NULL)
	{
		printf("fp1	open error\n");
		exit(1);
	
	}

	if(fp2==NULL)
	{
	  printf("fp2 open error");
	  exit(1);
	
	}



	while ((fscanf(fp1,"%s",tempstr)) !=EOF )
	
	{
	 	
 	//printf("%s 1 => %c \n",tempstr,tempstr[0]);
	//printf("%s 2 => %c \n",tempstr,tempstr[1]);
	
	
    
	
	temp=atof(tempstr);

	//printf("temp= %f\n ",temp );	
	
	


//	printf("%f",temp);
	if( ( temp == 0  && tempstr[0] =='0'&& tempstr[1] != ':' && tempstr[1]!='-' ) || (temp == 0 && tempstr[0] == '-' && tempstr[1] == '0'   ) || (temp!=0 && tempstr[1]!=':' && tempstr[2] != ':' && tempstr[3]!=':'  )	) 
	{ 
        
	   			
	   switch(insideconter)
	   {	   
		case 1:	
				fprintf(fp2,"1 %d:%.3f   ",insideconter,temp);
				insideconter++;
	    		break;
		
		case 39: 
			   fprintf(fp2,"%d:%.3f \n" ,insideconter,temp);
			   insideconter=1;
			   break;


		
		default:	

				fprintf(fp2,"%d:%.3f   ",insideconter,temp);
				insideconter++;
				break;

			}

		


 




	    
	}	
    




	}
	printf("over");
	fclose(fp1);
	fclose(fp2);




}
