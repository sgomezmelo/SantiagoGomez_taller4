#include<iostream>
#include<fstream>
#include<string>
#include<cmath>

using std::cout;
using std::cin;
using std::endl;
using std::string;
using std::ifstream;


double *time(double *t, int n){
  double dt = (t[n-1])/n - t[0]/n;
  double *tiempo = new double[n];
  tiempo[0] = t[0];
  for(int i = 1; i<n; i++){
    tiempo[i] = tiempo[i-1] + dt;
  }
  return tiempo;
}

double L_j(double t, double *tiempo, int j, int n){
  double resp = 1;
  for(int i = 0; i < n; i++){
    if(i != j){
      resp = resp * (t - tiempo[i])/(tiempo[j] - tiempo[i]);
    }
  }
  return resp;
}

double *fourier_real(double *x, int n){
  double *resp = new double[n];
  double pi = 3.1415926535897932;
  for(int i = 0; i < n; i++){
    double suma = 0;
    for(int j = 0; j<n; j++){
      suma = suma + x[j]*cos(-2*pi*j*i/n);
    }
    resp[i]  = suma/n;
  }
  return resp;
}

double *fourier_img(double *x, int n){
  double *resp = new double[n];
  double pi = 3.1415926535897932;
  for(int i = 0; i < n; i++){
    double suma = 0;
    for(int j = 0; j<n; j++){
      suma = suma + x[j]*sin(-2*pi*j*i/n);
    }
    resp[i]  = suma/n;
  }
  return resp;
}

double *w(double *tiempo, int n){
  double dt = tiempo[n-1]/n - tiempo[0]/n;
  double *resp = new double[n];
  for(int i = 0; i < n; i++){   
    resp[i] = (double)i/(double)n * 1.0/dt;
  }

  return resp;
}

int main(int argc, char* argv[]){
  string file_name = argv[1];
  string line;
  ifstream inputfile;
  int n = 0;
  inputfile.open(file_name);
  while ( getline (inputfile,line) )
    {
      n++;
    }
  double *t = new double[n];
  double *x = new double[n];
  inputfile.close();
  inputfile.open(file_name);
  for (int i = 0; i<n; i++)
    {
      double t_i;
      double x_i;
      inputfile >> t_i >> x_i;
      t[i] = t_i;
      x[i] = x_i;
    }
  double *tiempo = time(t,n);
  double *interpolacion = new double[n];

  for (int i = 0; i<n; i++)
    {
      double x_new = 0;
      for(int j = 0; j<n; j++){
	x_new = x_new + x[j]*L_j(tiempo[i], t, j, n);
      }
      interpolacion[i] = x_new;
    }
  
  double *Re = fourier_real(interpolacion,n);
  double *Im = fourier_img(interpolacion,n);
  double *freq = w(tiempo,n);
  for (int i = 0; i<n; i++)
    {
      cout << freq[i] << " " << Re[i] << " " << Im[i] << endl;
    }

  return 0;
}
  
  
  
  




