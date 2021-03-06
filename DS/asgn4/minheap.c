#include <stdio.h>
#include <stdlib.h>

typedef struct node
{
	long long ver;
	long long len;
}city;
long long tot=0;
long long count=0,deg[100005];
long long size=0,vis[100005]={0};
city arr[500005];
city *c[100005];
void heapify(long long i)
{
	long long leftl = arr[2*i].len;
	city left=arr[2*i],right=arr[2*i+1],root=arr[i];
	long long leftv = arr[2*i].ver;
	long long rightl = arr[2*i+1].len;
	long long rightv = arr[2*i+1].ver;
	long long rootl = arr[i].len;
	long long rootv= arr[i].ver;
	if(i>=1 && i<=size && (2*i+1<=size || 2*i<=size ))
	{
		if(( leftl <= rightl && leftl <= rootl) || (leftl<=rootl && 2*i+1>size))
		{
			arr[i] = left;
			arr[2*i] = root;
			heapify(2*i);
		}
		else if( rightl <= leftl && rightl <= rootl)
		{
			arr[i] = right;
			arr[2*i+1] = root;
			heapify(2*i+1);
		}
	}
}
city pop()
{
	city root;
	root.ver=arr[1].ver;
	root.len=arr[1].len;

	//	mrootl = arr[1].len;
	//	mrootv = arr[1].ver;
	arr[1]=arr[size];
	size--;
	if(size!=0)
		heapify(1);
	return root;
}
void insert(city val)
{
	size++;
	arr[size] = val;
	long long vall,valv;
	vall=val.len;
	valv=val.ver;
	long long parent = size/2;
	long long child = size;
	while(arr[parent].len > vall && parent >= 1)
	{
		//		if(
		arr[child] = arr[parent];
		arr[parent] = val;
		child = parent;
		parent = parent/2;
	}
	//	printf("len of root(min) = %lld\n",arr[1].len);
	return;
}
long long prim(long long vt,long long n)
{
	while(count!=n+1)
	{
		long long i,j;
		city roo;
		if(count==0)
			i=1;
		else
		{	
			roo=pop();
			i=roo.ver;
	//		printf("%lld\n",i);
	//		if(i==5)
	//			printf("yes\n");
		}
		count++;
		//if(i==5)
		//	printf("vis[%lld]=%lldyed\n ",i,vis[i]);
		if(vis[i]==0)
		{
			vis[i]=1;
			for(j=0;j<deg[i];j++)
			{
	//			if(i==4)
	//				printf("bhos%lld\n",c[i][j].ver);
					//	vis[c[i][j].ver]=1;
				if(vis[c[i][j].ver]==0)
					insert(c[i][j]);
			}
			if(count!=0)
			{
				tot=tot+roo.len;
//				printf("tot=%lld\n",tot);
			}
		}
	}
	//	printf("returned\n");
	return tot;
}
/*
//void formHeap(){
long int i;
for(i=size/2;i>=1;i--){
heapify(i);
}
}*/


//void print(){
//long long i;
//for(i=1;i<=size;i++)
//printf("%lld ",arr[i]);
//printf("\n");
//}//
void init(long long v, long long e)
{
	tot=0,count=0,size=0;
	long long i;
	for(i=1;i<500005;i++)
	{
		arr[i].ver=0;
		arr[i].len=0;
		vis[i]=0;
		deg[i]=0;
	}
	return;
}
int main()
{
	/*       long long n,i,j,k;
		 size = 0;
		 scanf("%lld",&n);

		 for(i=1;i<=n;i++)
		 {
		 scanf("%lld",&j);
		 insert(j);
		 }

		 print();
		 printf("%lld\n",pop());
		 print();
		 printf("%lld\n",pop());
		 print();

	 */
	long long t;
//	printf("1\t");
	scanf("%lld",&t);
	while(t--)
	{
		long long n,m,i,u[100005],v[100005],w[100005],total=0,ans,temp,max=0;
		long long ar[500050]={0},mi1,mi2;
//	printf("n,m\t");
		scanf("%lld %lld",&n,&m);
		init(n,m);
		for(i=0;i<m;i++)
		{
//	printf("u,v,w\t");
			scanf("%lld %lld %lld",&u[i],&v[i],&w[i]);
			deg[u[i]]++,deg[v[i]]++;
			total=total+w[i];
			if(w[i]>max)
			{
				max=w[i];
				mi1=v[i];
				mi2=u[i];
			}
		}
		for (i=1;i<=n;i++)
		{
			c[i]=(city *)malloc((deg[i]+2)*sizeof(city));
		}
		for(i=0;i<m;i++)
		{
			c[u[i]][ar[u[i]]].ver=v[i];
			c[u[i]][ar[u[i]]].len=w[i];
			ar[u[i]]++;
			c[v[i]][ar[v[i]]].ver=u[i];
			c[v[i]][ar[v[i]]].len=w[i];
			ar[v[i]]++;
		}
		long long j;
		//		for(i=1;i<=n;i++)
		//			for(j=0;j<deg[i];j++)
		//				printf("c[%lld][%lld]=%lld\n",i,j,c[i][j].ver);
		temp=prim(1,m);
		ans=total-temp;

//		if((vis[mi1]==0 &&  vis[mi2]!=0 ) || (vis[mi1]!=0 && vis[mi2]==0))
//			ans=ans-max;
		printf("%lld\n",ans);
//		printf("valjaiefiaekfmekjfaef vis[max]=%lld &  %lld \n",vis[mi1],vis[mi2]);

	}
	return 0;
}
