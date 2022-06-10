#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
/*#define _CRT_SECURE_NO_DEPRECATE*/

using namespace std;

/*
* Tr(KTr, Name, Grade) - Trainer
* SM(KTr, KT, Name) - SportsMan
* T(KT, ...) - Team
*/

typedef struct {
	char name[128];
	int grade;

} Trainer;


typedef struct {
	int kt;
	char name[128];
} SportsMan;

struct SportsManNode {
	SportsManNode(SportsMan* _sportsMan, const int& _numberSn, const int& _next) { sportsMan = *_sportsMan, previous = -1; next = _next; numberSn = _numberSn; }
	SportsManNode() { previous = -1; next = -1; numberSn = -1; }
	SportsMan sportsMan;
	int previous;
	int next;
	int numberSn;
};

struct TrainerNode {
	TrainerNode(const Trainer* tr, const int &_numberIndex) { firstSportsMan = -1; trainer = *tr; numberSportsMan = 0; numberIndex = _numberIndex; }
	TrainerNode() { firstSportsMan = -1; numberSportsMan = 0; numberIndex = -1; }
	int firstSportsMan;
	Trainer trainer;
	int numberSportsMan;
	int numberIndex;
};

struct TrainerIndexNode {
	TrainerIndexNode() { numberFl = -1; KTr = -1; }
	TrainerIndexNode(const int &_numberFl, const int &_KTr) { numberFl = _numberFl; KTr = _KTr; }
	int numberFl;
	int KTr;
};


template <typename T, typename N>
class FileConnector
{
public:
	FileConnector(const string &fileName, const ios_base::openmode &mode ,const int &sizeBlock, const ios_base::openmode &modeAd = NULL)
	{
		this->fileName = fileName;
		this->mode = mode;
		this->sizeBlock = sizeBlock;
		file.open(fileName, mode | ios_base::binary | modeAd);
		if (!file.is_open())
			throw exception("FileConnector");
		if ((GetSize() * sizeBlock) % sizeBlock != 0)
			throw exception("HealDamaged");
	}

	~FileConnector() { file.close(); }

	int GetSize()
	{
		if (mode != ios_base::app)
			file.seekg(0, ios_base::end);
		return ((int)file.tellg() / sizeBlock);
	}

	N ReadLast()
	{
		return this->Read(this->GetSize());
	}

	void WriteEnd(const N *node)
	{
		this->Write(node, (GetSize() + 1));
	}

	void Write(const N* node, const int& number)
	{
		if (number <= 0)
			throw exception("WriteNegative");
		if (typeid(T) == typeid(ifstream))
			throw exception("WriteInIfstream");
		file.seekg((number - 1) * sizeBlock, ios_base::beg);
		file.write((char*)node, sizeBlock);
	}

	N Read(const int& number)
	{
		if (number <= 0)
			throw exception("ReadNegative");
		if (typeid(T) == typeid(ofstream) || mode == ios_base::app)
			throw exception("ReadInOfstream");
		N node;
		file.seekg((number - 1) * sizeBlock, ios_base::beg);
		file.read((char*)&node, sizeBlock);
		return node;
	}

	void DeleteLast()
	{
		if (typeid(T) == typeid(ifstream) || mode == ios_base::app)
			throw exception("ReadInOfstream");
		int size = (GetSize() - 1) * sizeBlock;
		char* buf = new char[size];
		file.seekg(0, ios_base::beg);
		file.read(buf, size);
		file.close();
		ofstream tempFile(fileName, ios_base::out, ios_base::binary);
		if (!tempFile.is_open())
			throw exception("DeleteLast");
		tempFile.write(buf, size);
		tempFile.close();
		delete[] buf;
		file.open(fileName);
		if (!file.is_open())
			throw exception("DeleteLast");
	}

	T& GetFile() { return file; }
private:
	T file;
	ios_base::openmode mode;
	int sizeBlock;
	string fileName;
};

class DbConnector
{
public:
	DbConnector(bool isTrunc = false)
	{
		//create files
		ofstream fileSFl (fileSFlName, (isTrunc ? ios_base::out : ios_base::app) | ios_base::binary);
		ofstream fileSInd(fileSIndName, (isTrunc ? ios_base::out : ios_base::app) | ios_base::binary);
		ofstream fileSpFl(fileSpFlName, (isTrunc ? ios_base::out : ios_base::app) | ios_base::binary);
		if (!fileSFl.is_open() || !fileSInd.is_open() || !fileSpFl.is_open())
			throw exception("ConstructorDbConnector");
		fileSFl.close();
		fileSInd.close();
		fileSpFl.close();
	}

	int InsertM(Trainer* tr)
	{
		if (tr == nullptr)
			throw exception("InsertMNull");
		FileConnector<fstream, TrainerNode> fileSFl(fileSFlName, ios_base::in, sizeof(TrainerNode), iostream::out);
		FileConnector<fstream, TrainerIndexNode> fileSInd (fileSIndName, ios_base::in, sizeof(TrainerIndexNode), ios_base::out);

		TrainerNode* trn = new TrainerNode(tr, fileSInd.GetSize() + 1);
		TrainerIndexNode* trin = new TrainerIndexNode((fileSFl.GetSize() + 1), fileSInd.GetSize() != 0 ? (fileSInd.ReadLast().KTr + 1) : 1);

		fileSFl.WriteEnd(trn);
		fileSInd.WriteEnd(trin);

		int KTr = trin->KTr;
		delete trn;
		delete trin;

		return KTr;
	}

	bool InsertS(int KTr, SportsMan* sp)
	{
		if (sp == nullptr)
			throw exception("InsertSNull");
		FileConnector<fstream, TrainerNode> fileSFl(fileSFlName, ios_base::in, sizeof(TrainerNode), iostream::out);
		FileConnector<fstream, SportsManNode> fileSpFl(fileSpFlName, ios_base::in, sizeof(SportsManNode), iostream::out);

		int numberTrn = GetM(KTr);
		if (numberTrn < 0)
			return false;
		for (int i = 0; i < fileSpFl.GetSize(); i++)
		{
			SportsManNode temp = fileSpFl.Read((i + 1));
			if (temp.sportsMan.kt == sp->kt)
				return false;
		}

		TrainerNode trn = fileSFl.Read(numberTrn);
		SportsManNode* newFirstSmn = new SportsManNode(sp, numberTrn, trn.firstSportsMan);
		int numberSmn = fileSpFl.GetSize() + 1;

		if (trn.firstSportsMan != -1)
		{
			SportsManNode oldFirstSmn = fileSpFl.Read(trn.firstSportsMan);
			oldFirstSmn.previous = numberSmn;
			fileSpFl.Write(&oldFirstSmn, trn.firstSportsMan);
		}

		trn.firstSportsMan = numberSmn;
		trn.numberSportsMan = trn.numberSportsMan + 1;
		fileSFl.Write(&trn, numberTrn);
		fileSpFl.WriteEnd(newFirstSmn);

		delete newFirstSmn;
		return true;
	}

	int GetS(int KTr, int KT)
	{
		FileConnector<ifstream, TrainerNode> fileSFl(fileSFlName, ios_base::in, sizeof(TrainerNode));
		FileConnector<ifstream, SportsManNode> fileSpFl(fileSpFlName, ios_base::in, sizeof(SportsManNode));

		int numberTrn = GetM(KTr);
		if (numberTrn < 0)
			return -1;
		TrainerNode trn = fileSFl.Read(numberTrn);
		if (trn.firstSportsMan < 0)
			return -1;

		int numberSmn = -1;
		SportsManNode smn = fileSpFl.Read(trn.firstSportsMan);
		if (smn.sportsMan.kt == KT)
		{
			numberSmn = trn.firstSportsMan;
		}
		else
		{
			int number = smn.next;
			for (int i = 1; i < trn.numberSportsMan; i++)
			{
				smn = fileSpFl.Read(smn.next);
				if (smn.sportsMan.kt == KT)
				{
					numberSmn = number;
					break;
				}
				number = smn.next;
				
			}
		}
		return numberSmn;
	}

	int GetM(int KTr)
	{
		return this->BinarySearchNumberFl(KTr);
	}	

	bool UpdateM(int KTr, string field, char value[128])
	{
		int numberTr = GetM(KTr);
		if (numberTr < 0)
			return false;
		FileConnector<fstream, TrainerNode> fileSFl(fileSFlName, ios_base::in, sizeof(TrainerNode), iostream::out);
		TrainerNode trn = fileSFl.Read(numberTr);

		if (field == "name")
			memcpy((void*)&trn.trainer.name, (void*)value, 128);
		else if (field == "grade")
			memcpy((void*)&trn.trainer.grade, (void*)value, sizeof(int));
		else
			return false;

		fileSFl.Write(&trn, numberTr);
		return true;
	}

	bool UpdateS(int KTr, int KT, string field, char value[128])
	{
		int numberSmn = GetS(KTr, KT);
		if (numberSmn < 0)
			return false;
		FileConnector<fstream, SportsManNode> fileSpFl(fileSpFlName, ios_base::in, sizeof(SportsManNode), iostream::out);
		SportsManNode smn = fileSpFl.Read(numberSmn);

		if (field == "name")
			memcpy((void*)&smn.sportsMan.name, (void*)value, 128);
		else
			return false;

		fileSpFl.Write(&smn, numberSmn);
		return true;
	}

	bool DelS(int numberSmn)
	{
		FileConnector<fstream, TrainerNode> fileSFl(fileSFlName, ios_base::in, sizeof(TrainerNode), ios_base::out);
		FileConnector<fstream, SportsManNode> fileSpFl(fileSpFlName, ios_base::in, sizeof(SportsManNode), ios_base::out);

		SportsManNode smn = fileSpFl.Read(numberSmn);
		TrainerNode trn = fileSFl.Read(smn.numberSn);
		if (smn.previous > 0)
		{
			SportsManNode smnPrevious = fileSpFl.Read(smn.previous);
			if (smn.next != -1)
				smnPrevious.next = smn.next;
			else
				smnPrevious.next = -1;
			fileSpFl.Write(&smnPrevious, smn.previous);
		}
		if (smn.next > 0)
		{
			SportsManNode smnNext = fileSpFl.Read(smn.next);
			if (smn.previous != -1)
				smnNext.previous = smn.previous;
			else
			{
				smnNext.previous = -1;
				trn.firstSportsMan = smn.next;
			}
			fileSpFl.Write(&smnNext, smn.next);
		}
		if (smn.next == -1 && smn.previous == -1)
			trn.firstSportsMan = -1;
		trn.numberSportsMan = trn.numberSportsMan - 1;
		fileSFl.Write(&trn, smn.numberSn);

		SportsManNode smnLast = fileSpFl.ReadLast();
		fileSpFl.Write(&smnLast, numberSmn);
		if (fileSpFl.GetSize() != numberSmn)
		{
			if (smnLast.previous == -1)
			{
				TrainerNode trn = fileSFl.Read(smnLast.numberSn);
				trn.firstSportsMan = numberSmn;
				fileSFl.Write(&trn, smnLast.numberSn);
			}
			else
			{
				SportsManNode smnPrevious = fileSpFl.Read(smnLast.previous);
				smnPrevious.next = numberSmn;
				fileSpFl.Write(&smnPrevious, smnLast.previous);
			}
			if (smnLast.next > 0)
			{
				SportsManNode smnNext = fileSpFl.Read(smnLast.next);
				smnNext.previous = numberSmn;
				fileSpFl.Write(&smnNext, smnLast.next);
			}
		}
		fileSpFl.DeleteLast();
		return true;
	}

	bool DelS(int KTr, int KT)
	{

		int numberSmn = GetS(KTr, KT);
		if (numberSmn < 0)
			return false;
		if (DelS(numberSmn))
			return true;
		return false;
	}

	bool DelM(int KTr)
	{
		FileConnector<fstream, TrainerNode> fileSFl(fileSFlName, ios_base::in, sizeof(TrainerNode), ios_base::out);
		FileConnector<fstream, TrainerIndexNode> fileSInd(fileSIndName, ios_base::in, sizeof(TrainerIndexNode), ios_base::out);
		FileConnector<fstream, SportsManNode> fileSpFl(fileSpFlName, ios_base::in, sizeof(SportsManNode), ios_base::out);

		int numberTrn = GetM(KTr);
		if (numberTrn < 0)
			return false;
		TrainerNode trn = fileSFl.Read(numberTrn);

		int cur = trn.firstSportsMan;
		for (int i = 0; i < trn.numberSportsMan; i++)
		{
			int smnNext = fileSpFl.Read(cur).next;
			fileSpFl.GetFile().close();
			if (!DelS(cur))
				return false;
			fileSpFl.GetFile().open(fileSpFlName);
			cur = smnNext;
		}

		TrainerNode trnLast = fileSFl.ReadLast();
		fileSFl.Write(&trnLast, numberTrn);
		fileSFl.DeleteLast();
		if (fileSFl.GetSize() > 0)
		{
			cur = trnLast.firstSportsMan;
			for (int i = 0; i < trnLast.numberSportsMan; i++)
			{
				SportsManNode smn = fileSpFl.Read(cur);
				smn.numberSn = numberTrn;
				cur = smn.next;
			}
		}

		TrainerIndexNode trinSnLast = fileSInd.Read(trnLast.numberIndex);
		trinSnLast.numberFl = numberTrn;
		fileSInd.Write(&trinSnLast, trnLast.numberIndex);

		cur = trn.numberIndex;
		for (int i = 0; i < fileSInd.GetSize() - trn.numberIndex; i++)
		{
			TrainerIndexNode curNext = fileSInd.Read(cur + 1);
			TrainerNode tempSn = fileSFl.Read(curNext.numberFl);
			tempSn.numberIndex = tempSn.numberIndex - 1;
			fileSFl.Write(&tempSn, curNext.numberFl);
			fileSInd.Write(&curNext, cur);
			cur = cur + 1;
		}
		fileSInd.DeleteLast();

		return true;
	}

	Trainer* ReadTrainer(int numberFl)
	{
		if (numberFl < 0)
			return nullptr;
		FileConnector<ifstream, TrainerNode> fileSFl(fileSFlName, ios_base::in, sizeof(TrainerNode));
		return new Trainer{ fileSFl.Read(numberFl).trainer };
	}

	SportsMan* ReadSportsMan(int numberSpFl)
	{
		if (numberSpFl < 0)
			return nullptr;
		FileConnector<ifstream, SportsManNode> fileSpFl(fileSpFlName, ios_base::in, sizeof(SportsManNode));
		return new SportsMan{ fileSpFl.Read(numberSpFl).sportsMan };
	}

	void Print()
	{
		FileConnector<ifstream, SportsManNode> fileSpFl(fileSpFlName, ios_base::in, sizeof(SportsManNode));
		FileConnector<ifstream, TrainerIndexNode> fileSInd(fileSIndName, ios_base::in, sizeof(TrainerIndexNode));
		FileConnector<ifstream, TrainerNode> fileSFl(fileSFlName, ios_base::in, sizeof(TrainerNode));
		for (int i = 0; i < fileSInd.GetSize(); i++)
		{
			TrainerIndexNode trin = fileSInd.Read(i + 1);
			TrainerNode trn = fileSFl.Read(trin.numberFl);
			cout << "KTr: " << trin.KTr << " " << "name: " << trn.trainer.name << " " << "grade: " << trn.trainer.grade << endl;
			int cur = trn.firstSportsMan;
			for (int i = 0; i < trn.numberSportsMan; i++)
			{
				SportsManNode smn = fileSpFl.Read(cur);
				cout << "   ";
				cout << "KTr: " << trin.KTr << " " << "KT: " << smn.sportsMan.kt << " " << "name: " << smn.sportsMan.name << endl;
				cur = smn.next;
			}
		}
	}

private:
	string fileSFlName = "S.fl";
	string fileSIndName = "S.ind";
	string fileSpFlName = "Sp.fl";

	int BinarySearchNumberFl(int KTr)
	{
		FileConnector<ifstream, TrainerIndexNode> fileSInd(fileSIndName, ios_base::in, sizeof(TrainerIndexNode));
		TrainerIndexNode trin;

		int left = 1, right = fileSInd.GetSize() + 1;
		while (left <= right)
		{
			int middle = (left + right) / 2;
			trin = fileSInd.Read(middle);
			if (trin.KTr > KTr)
				right = middle - 1;
			else if (trin.KTr < KTr)
				left = middle + 1;
			else
				return trin.numberFl;
		}
		return -1;
	}
};

void PrintInfo()
{
	cout << "Commands: " << endl;
	cout << "insert-m [name] [grade]" << endl;
	cout << "insert-s [KTr] [KT] [name]" << endl;
	cout << "get-m [KTr]" << endl;
	cout << "get-s [KTr] [KT]" << endl;
	cout << "update-m [KTr] [field] [value]" << endl;
	cout << "update-s [KTr] [KT] [field] [value]" << endl;
	cout << "del-m [KTr]" << endl;
	cout << "del-s [KTr] [KT]" << endl;
	cout << "print" << endl;
	cout << "exit" << endl << endl;
}

int main() {
	setlocale(LC_ALL, "Russian");
	DbConnector st;
	string command;
	try {
		PrintInfo();
		while (true)
		{
			cin >> command;
			if (command == "insert-m")
			{
				Trainer tr = {};
				cin >> tr.name >> tr.grade;
				cout << "Added Successfully KTr: " << st.InsertM(&tr) << endl;
			}
			else if (command == "get-m")
			{
				int KTr;
				cin >> KTr;
				Trainer* tr = st.ReadTrainer(st.GetM(KTr));
				if (tr == nullptr)
					cout << "Trained don't found" << endl;
				else
					cout << tr->name << " " << tr->grade << endl;
				delete tr;
			}
			else if (command == "insert-s")
			{
				SportsMan sm = {};
				int KTr;
				cin >> KTr >> sm.kt >> sm.name;
				if (st.InsertS(KTr, &sm))
					cout << "Added" << endl;
				else
					cout << "Not Added" << endl;

			}
			else if (command == "get-s")
			{
				int KTr, KT;
				cin >> KTr >> KT;
				SportsMan* r = st.ReadSportsMan(st.GetS(KTr, KT));
				if (r == nullptr)
					cout << "Rent don't found" << endl;
				else
					cout << r->kt << " " << r->name << endl;
				delete r;
			}
			else if (command == "update-m")
			{
				int KTr;
				string field;
				char value[128];
				cin >> KTr >> field;
				if (field == "grade")
				{
					int number;
					cin >> number;
					memcpy((void*)value, (void*)&number, sizeof(int));
				}
				else
					cin >> value;
				if (st.UpdateM(KTr, field, value))
					cout << "Successfully updated" << endl;
				else
					cout << "Failure" << endl;
			}
			else if (command == "update-s")
			{
				int KS, KB;
				string field;
				char value[128];
				cin >> KS >> KB >> field >> value;
				if (st.UpdateS(KS, KB, field, value))
					cout << "Successfully updated" << endl;
				else
					cout << "Failure" << endl;
			}
			else if (command == "del-m")
			{
				int KTr;
				cin >> KTr;
				if (st.DelM(KTr))
					cout << "Successfully deleted" << endl;
				else
					cout << "Failure" << endl;
			}
			else if (command == "del-s")
			{
				int KTr, KT;
				cin >> KTr >> KT;
				if (st.DelS(KTr, KT))
					cout << "Successfully deleted" << endl;
				else
					cout << "Failure" << endl;
			}
			else if (command == "print")
			{
			st.Print();
 }
			else if (command == "exit")
			{
				break;
			}
			else
			{
				cout << "Wrong Command" << endl;
			}
		}
	}
	catch (exception& ex)
	{
		cout << ex.what();
	}

	return 0;
}
