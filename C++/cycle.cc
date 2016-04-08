#include<iostream>
#include<vector>

/**
 1	2	3	4	5	6
 20	21	22	23	24	7
 19	32	33	34	25	8
 18	31	36	35	26	9
 17	30	29	28	27	10
 16	15	14	13	12	11
**/


using namespace std;

void cons(vector<vector<int> > &matrix, int x, int y, int w, int h, int start) {
	if (w <= 0 || h <= 0) {
		return;
	}else{
		for (int i = x;i < x + w - 1; ++i) {
			matrix[x][i] = ++start;
		}
		for (int i = y;i < y + h; ++i) {
			matrix[i][x + w - 1] = ++start;
		}
		for (int i = x + w - 2; i > x && h!=1;--i) {
			matrix[y + h - 1][i] = ++start;
		}
		for (int i = y + h - 1;i > y && w!=1;--i) {
			matrix[i][y] = ++start;
		}
		cons(matrix, x + 1, y + 1, w - 2, h - 2, start);
	}
}

int main() {
	int r = 0, c = 0;
	cin >> r >> c;
	vector<vector<int> > matrix(r, vector<int>(c, 0));
	cons(matrix, 0, 0, c, r, 0);
	for (auto row : matrix) {
		for (auto i : row) {
			cout << i << "\t";
		}
		cout << endl;
	}
}
