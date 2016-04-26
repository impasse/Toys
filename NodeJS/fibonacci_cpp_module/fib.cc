#include<vector>
#include<gmpxx.h>
#include<node/node.h>


namespace fib{
	using namespace std;
	using namespace v8;

	mpz_class fib(vector<mpz_class>::size_type n){
		auto arr = new vector<mpz_class>(n+1,0);
		arr->operator[](0) = 0;
		arr->operator[](1) = 1;
		vector<mpz_class>::size_type pos = 2;
		while(pos<=n){
			arr->operator[](pos) = arr->operator[](pos-2)+arr->operator[](pos-1);
			pos++;
		}
		return arr->operator[](n);
	}

	void getFib(const FunctionCallbackInfo<Value>& args){
		Isolate* isolate = args.GetIsolate();
		int argc = args.Length();
		if(argc==1 && args[0]->IsNumber()){
			auto  n = static_cast<long long>(args[0]->NumberValue());
			args.GetReturnValue().Set(String::NewFromUtf8(isolate,fib(n).get_str().c_str()));
		}else{
			args.GetReturnValue().Set(Number::New(isolate,0));
		}

	}

	void initializer(Local<Object> exports,Local<Object> module){
		NODE_SET_METHOD(module,"exports",getFib);
	}

	NODE_MODULE(fib,initializer);
}
