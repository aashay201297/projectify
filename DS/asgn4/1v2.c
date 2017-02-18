#include<stdio.h>
long long count[100004],val[100005];
//x[100005];
void init(long long a)
{
	long long i;
	for(i=0;i<100004;i++)
	{
		count[i]=0;
//		x[i]=0;
	}
return;
}
/*long long find(long long a)
{
	long long i,temp=0,flag=0;
	for(i=1;i<=a;i++)
	{
		temp=temp+(i*x[i])/2 ;
		if(x[i]%2==1)
			flag++;
		if(flag==0)
		{
			temp+=x[i]%2;
		}
		else
	}
//	printf("temp=%lld\n",temp);
	return temp;
}*/
int main ()
{
	long long t;
	scanf("%lld",&t);
	while(t--)
	{
		long long i,n,ans=0,ansF,mfreq=-100;
		scanf("%lld",&n);
		init(n);
		for(i=1;i<=n;i++)
		{
			scanf("%lld",&val[i]);
			count[val[i]]++;
			if(count[val[i]] > mfreq)
				mfreq=count[val[i]];

		//	x[count[val[i]]]++;
		//	if(count[val[i]]!=1)
		//		x[count[val[i]]-1]--;
			
		}
		if(n > 2*mfreq)
		{
			ans = n/2 + n%2;
		}
		else
		{
			ans=mfreq;
		}
		printf("%lld\n",ans);
	}
	return 0;
}
