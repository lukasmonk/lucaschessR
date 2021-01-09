/*
You can use this program under the terms of either the following zlib-compatible license
or as public domain (where applicable)

  Copyright (C) 2012-2015 Martin Sedlak

  This software is provided 'as-is', without any express or implied
  warranty.  In no event will the authors be held liable for any damages
  arising from the use of this software.

  Permission is granted to anyone to use this software for any purpose,
  including commercial applications, and to alter it and redistribute it
  freely, subject to the following restrictions:

  1. The origin of this software must not be misrepresented; you must not
     claim that you wrote the original software. If you use this software
     in a product, an acknowledgement in the product documentation would be
     appreciated but is not required.
  2. Altered source versions must be plainly marked as such, and must not be
     misrepresented as being the original software.
  3. This notice may not be removed or altered from any source distribution.
*/

#include "tune.h"
#include "eval.h"

#include <iostream>
#include <fstream>
#include <algorithm>

namespace cheng4
{

std::vector<Feature> features;
std::vector<i16> featureVector;

static const i16 optimizedFeatureVector[] = {
	-91, 19, -16, -31, -37, -40, -15,
	0, 67, 97, 225, 320, 467, 688, 854,
	969, 1420, 1647, 2178, 2620, 2210, 2992, 0,
	2624, 2, 2248, 1, -4, 0, -1, 123,
	25, -5, 119, 153, 407, 740, 34, -49,
	63, 66, 157, 317, 403, 78, 385, 569,
	-10, -48, 98, 73, 157, 56, 316, 312,
	402, 1011, 93, 341, 339, 550, 1021, 12,
	12, 5, 4, 7, -10, 18, 11, 15,
	15, 218, 163, 326, 567, 1022, 872, 2645,
	-17, 69, 28, 111, 405, 366, 392, 529,
	496, 327, 193, 4, 422, 125, 2, 49,
	88, 22, 130, 184, 216, 146, 115, 85,
	0, 0, -112, 55, 110, 34, 86, 205,
	1107, 235, 118, 17, 10, 75, 211, 558,
	0, -1, 47, 166, 357, 992, 0, 38,
	-109, -121, -8, 369, 946, 174, 159, 439,
	756, 1269, 1852, -472, -319, -238, -181, -131,
	-94, -37, 22, 128, -461, -520, -293, -156,
	-58, 51, 53, 55, -30, -259, -158, -63,
	-7, 38, 66, 79, 54, 42, 65, 89,
	59, 302, 624, -313, -221, -126, -34, 74,
	146, 194, 222, 234, 222, 194, 213, 151,
	243, 38, 68, 125, 82, 64, 113, 146,
	208, 251, 326, 387, 328, 376, 575, -75,
	-332, -4, 113, 252, 309, 354, 402, 438,
	494, 525, 562, 577, 583, 500, 638, 111,
	215, 356, 382, 389, 375, 380, 371, 363,
	364, 386, 401, 410, 513, 589, 786, 1037,
	1586, 1740, 1873, 1409, 1912, 926, 690, -933,
	-3949, 3914, 1167, -63, 198, 267, 463, 548,
	631, 679, 774, 850, 918, 948, 965, 986,
	934, 952, 913, 874, 795, 807, 801, 810,
	822, 821, 921, 897, 1091, 848, 1250, 951,
	-111, 45, -30, -60, 42, 66, 81, 35,
	79, 150, 137, 173, 148, 292, 271, 666,
	-2084, -144, -104, -194, -58, -63, -20, -6,
	172, 69, 106, 151, 174, 188, 253, 453,
	-247, 112, 15, 57, 92, 74, -20, -144,
	-92, 7, 3, 32, 27, 43, 63, 23,
	15, 4, 7, 7, 18, 24, 29, 1,
	6, -4, 1, 8, 12, 17, 19, 9,
	8, -9, -5, -4, -4, 9, -5, 14,
	0, -11, -7, -6, -9, -4, 13, 26,
	-10, 54, 59, 52, 18, 7, 19, 55,
	38, 44, 37, 15, -10, -22, 4, 14,
	13, 27, 15, -1, -19, -14, -10, 0,
	1, 14, 8, -5, -12, -9, -4, -2,
	-8, 10, 4, -4, -5, 0, -2, -2,
	-7, 12, 6, -1, 4, 5, 8, 1,
	-11, -186, -118, -51, -19, 35, -116, -66,
	-172, -15, -17, 0, 27, -19, 46, -26,
	-4, -25, -2, 8, 19, 77, 52, 25,
	-35, -9, 6, 15, 28, 6, 35, 8,
	23, 2, 17, 12, 9, 11, 15, 6,
	6, -17, -4, 1, 9, 18, 8, 13,
	-10, 1, -5, -9, 6, 7, 7, -1,
	4, -47, -16, -7, 1, 1, 9, -9,
	-53, -6, -2, 0, 17, 4, -6, -5,
	-55, -1, 9, 5, 14, 11, 2, -2,
	-6, 1, 4, 20, 24, 12, 29, 7,
	1, 11, 6, 17, 22, 17, 22, 14,
	11, 7, 2, 20, 18, 28, 16, 13,
	10, -19, -2, -1, 15, 16, 3, 4,
	1, -39, -8, -14, 2, 5, -2, 5,
	-1, -55, -11, -12, -2, -1, -6, 2,
	-23, -44, -46, -101, -62, -89, -120, -18,
	30, -42, -24, -28, -50, -42, -87, -78,
	-67, -12, -4, -12, 8, -1, 61, -5,
	7, -24, -8, 1, 23, 4, -10, -3,
	-29, -28, 1, -9, 9, -1, -10, -9,
	-1, -11, -5, -1, -7, -3, 0, 5,
	1, -1, -1, -1, -9, 0, 7, 20,
	12, 2, 20, -13, -10, 10, -12, 7,
	-3, 6, 13, 6, 16, 6, -4, 5,
	-6, 15, 6, 6, 2, 6, 5, 10,
	-10, -3, 14, 10, 7, 12, 27, 21,
	0, 2, 10, 15, 23, 19, 15, 7,
	5, -9, 2, 12, 22, 19, 7, 4,
	-9, -6, 4, 13, 5, 18, 4, 1,
	-7, -6, -4, -5, 2, -4, 3, 1,
	-29, -6, -9, 1, -3, -5, 0, -13,
	-16, -4, 3, -9, 4, -20, 0, 45,
	95, 1, -15, 14, 28, 30, 44, 49,
	78, -13, 17, -5, 17, 56, 55, 73,
	41, -17, -15, 10, 24, 22, 16, 21,
	28, -34, -26, -10, -8, -12, -14, 7,
	-23, -27, -14, -11, -18, 0, -20, 5,
	-28, -33, -21, -12, -6, -11, -3, 3,
	-31, -12, -8, -6, 0, 1, -3, 3,
	-8, 13, 21, 20, 21, 22, 23, 20,
	20, 27, 28, 32, 33, 30, 21, 24,
	24, 27, 24, 28, 27, 24, 24, 21,
	23, 25, 29, 28, 26, 22, 25, 22,
	18, 12, 18, 18, 13, 12, 15, 13,
	5, -5, 0, -3, 0, -2, 1, 2,
	-12, -18, -7, -2, -7, -6, -10, -8,
	-16, -13, -12, -5, -5, -10, -8, -9,
	-19, -27, -42, -55, -70, -48, -48, 130,
	59, -20, -35, -3, -12, -29, -11, -5,
	58, -16, -11, -20, -12, -15, 67, 36,
	18, -10, -6, -6, -16, -13, -5, 0,
	-3, -11, -10, -11, -10, -14, -9, 2,
	-18, -9, -2, -6, -12, -6, -3, 8,
	5, -16, -6, 1, 5, 3, 10, 33,
	-9, -9, -8, 4, 1, -11, 4, -5,
	-7, 9, 20, 31, 35, 33, 37, 20,
	30, 13, 27, 40, 48, 47, 31, 31,
	43, 10, 29, 39, 45, 54, 40, 34,
	29, 8, 26, 37, 44, 46, 35, 44,
	33, 4, 13, 20, 33, 29, 22, 27,
	23, -7, -3, 7, 4, 17, 12, 13,
	1, -19, -10, -12, -12, -5, -29, -44,
	-14, -23, -22, -21, -18, -11, -51, -47,
	-24, -395, 37, 17, -331, -19, -104, 16,
	80, 66, 32, -7, -76, -95, -1, 1,
	27, 46, -85, -109, 60, -135, -175, -27,
	-1, 47, 34, -68, -185, -179, -128, -127,
	-205, -19, -36, -77, -213, -168, -153, -163,
	-132, -132, 14, -96, -126, -95, -104, -85,
	-55, -13, -105, -55, -110, -81, -68, -18,
	-9, -38, -10, 6, -73, 1, -59, 19,
	21, -154, -34, -20, 1, 0, 16, 20,
	-112, -45, 21, 25, 21, 41, 47, 63,
	-35, 8, 30, 39, 44, 39, 61, 56,
	25, -1, 17, 35, 40, 43, 45, 41,
	12, -20, 11, 24, 34, 33, 29, 19,
	-6, -29, -5, 10, 21, 22, 15, 4,
	-11, -16, -8, 2, 2, 4, 2, -5,
	-17, -46, -18, -12, -21, -36, -20, -23,
	-42
};

void addFeature(const char *name, i16 *ptr, int count)
{
	Feature feat;
	feat.name = name;
	feat.table = ptr;
	feat.size = count;
	feat.start = (int)featureVector.size();

	features.push_back(feat);

	for (int i=0; i<feat.size; i++)
		featureVector.push_back(ptr[i]);
}

bool saveFeatures(const char *filename)
{
	std::ofstream ofs( filename, std::ios::out );

	if (!ofs.is_open())
		return 0;

	ofs << "\t";

	for (size_t i=0; i<featureVector.size(); i++)
	{
		if ((i & 7) == 7)
			ofs << std::endl << "\t";

		ofs << featureVector[i];

		if (i+1 < featureVector.size())
			ofs << ", ";
	}

	ofs << std::endl;
	return 1;
}

#define ADD_SINGLE_FEATURE(x) addFeature(#x, &x)

void extractFeatures()
{
	addFeature("kingCheckPotential", kingCheckPotential, 28);

	ADD_SINGLE_FEATURE(progressBasePly);
	ADD_SINGLE_FEATURE(progressScale);

	ADD_SINGLE_FEATURE(disconnectedPawn);
	ADD_SINGLE_FEATURE(disconnectedPawnEg);

	addFeature("connectedPasserOpening", connectedPasserOpening+1, 6);
	addFeature("connectedPasserEndgame", connectedPasserEndgame+1, 6);

	addFeature("kingOpenFile", kingOpenFile+1, 3);
	addFeature("kingOpenFileEndgame", kingOpenFileEg+1, 3);

	ADD_SINGLE_FEATURE(rookBehindPasserOpening);
	ADD_SINGLE_FEATURE(rookBehindPasserEndgame);

	addFeature("materialOpening", PSq::materialTables[phOpening]+1, 5);
	addFeature("materialEndgame", PSq::materialTables[phEndgame]+1, 5);

	addFeature("safetyScale", safetyScale+1, 5);
	addFeature("safetyScaleEg", safetyScaleEg+1, 5);

	ADD_SINGLE_FEATURE(shelterFront1);
	ADD_SINGLE_FEATURE(shelterFront2);

	ADD_SINGLE_FEATURE(bishopPairOpening);
	ADD_SINGLE_FEATURE(bishopPairEndgame);

	ADD_SINGLE_FEATURE(trappedBishopOpening);
	ADD_SINGLE_FEATURE(trappedBishopEndgame);

	ADD_SINGLE_FEATURE(unstoppablePasser);

	ADD_SINGLE_FEATURE(doubledPawnOpening);
	ADD_SINGLE_FEATURE(doubledPawnEndgame);

	ADD_SINGLE_FEATURE(isolatedPawnOpening);
	ADD_SINGLE_FEATURE(isolatedPawnEndgame);

	ADD_SINGLE_FEATURE(knightHangingOpening);
	ADD_SINGLE_FEATURE(knightHangingEndgame);

	ADD_SINGLE_FEATURE(bishopHangingOpening);
	ADD_SINGLE_FEATURE(bishopHangingEndgame);

	ADD_SINGLE_FEATURE(rookHangingOpening);
	ADD_SINGLE_FEATURE(rookHangingEndgame);

	ADD_SINGLE_FEATURE(rookOnOpenOpening);
	ADD_SINGLE_FEATURE(rookOnOpenEndgame);

	ADD_SINGLE_FEATURE(queenHangingOpening);
	ADD_SINGLE_FEATURE(queenHangingEndgame);

	ADD_SINGLE_FEATURE(kingPasserSupportBase);
	ADD_SINGLE_FEATURE(kingPasserSupportScale);

	addFeature("outpostBonusFile", outpostBonusFile, 8);
	addFeature("outpostBonusRank", outpostBonusRank, 8);

	ADD_SINGLE_FEATURE(pawnRaceAdvantageEndgame);

	addFeature("passerScaleImbalance", passerScaleImbalance, 1);
	addFeature("passerScaleBlocked", passerScaleBlocked, 1);

	addFeature("candPasserOpening", candPasserOpening+1, 6);
	addFeature("candPasserEndgame", candPasserEndgame+1, 6);

	addFeature("passerOpening", passerOpening+1, 6);
	addFeature("passerEndgame", passerEndgame+1, 6);

	addFeature("knightMobilityOpening", knightMobility[phOpening], 9);
	addFeature("knightMobilityEndgame", knightMobility[phEndgame], 9);

	addFeature("bishopMobilityOpening", bishopMobility[phOpening], 14);
	addFeature("bishopMobilityEndgame", bishopMobility[phEndgame], 14);

	addFeature("rookMobilityOpening", rookMobility[phOpening], 15);
	addFeature("rookMobilityEndgame", rookMobility[phEndgame], 15);

	addFeature("queenMobilityOpening", queenMobility[phOpening], 28);
	addFeature("queenMobilityEndgame", queenMobility[phEndgame], 28);

	addFeature("goodBishopOpening", goodBishopOpening, 17);
	addFeature("goodBishopEndgame", goodBishopEndgame, 17);

	// and finally piece-square tables

	addFeature("pawnPsqOpening", PSq::pawnTables[phOpening] + 8, 64-2*8);
	addFeature("pawnPsqEndgame", PSq::pawnTables[phEndgame] + 8, 64-2*8);

	addFeature("knightPsqOpening", PSq::knightTables[phOpening], 64);
	addFeature("knightPsqEndgame", PSq::knightTables[phEndgame], 64);

	addFeature("bishopPsqOpening", PSq::bishopTables[phOpening], 64);
	addFeature("bishopPsqEndgame", PSq::bishopTables[phEndgame], 64);

	addFeature("rookPsqOpening", PSq::rookTables[phOpening], 64);
	addFeature("rookPsqEndgame", PSq::rookTables[phEndgame], 64);

	addFeature("queenPsqOpening", PSq::queenTables[phOpening], 64);
	addFeature("queenPsqEndgame", PSq::queenTables[phEndgame], 64);

	addFeature("kingPsqOpening", PSq::kingTables[phOpening], 64);
	addFeature("kingPsqEndgame", PSq::kingTables[phEndgame], 64);

	// load actual optimized values

	size_t optsz = sizeof(optimizedFeatureVector) / sizeof(i16);

	optsz = std::min(optsz, featureVector.size());

	for (size_t i=0; i<optsz; i++)
		featureVector[i] = optimizedFeatureVector[i];

	for (size_t i=0; i<features.size(); i++)
	{
		const Feature &ft = features[i];

		for (int j=0; j<ft.size; j++)
			ft.table[j] = featureVector[ft.start + j];
	}

	// re-init psq to bake material into them
	PSq::init();
}

#undef ADD_SINGLE_FEATURE

}

#ifdef USE_TUNING

#include <iostream>

namespace cheng4
{

// TunableParams

TunableParams *TunableParams::inst = 0;

TunableParams *TunableParams::get()
{
	// note: not thread-safe
	if ( !inst )
		inst = new TunableParams;
	return inst;
}

std::vector< TunableBase * > TunableParams::params;

void TunableParams::addParam( TunableBase *param )
{
	params.push_back( param );
}

bool TunableParams::setParam( const char *name, const char *value )
{
	for ( size_t i=0; i<params.size(); i++ )
	{
		if ( params[i]->name() == name )
		{
			params[i]->set( value );
			return 1;
		}
	}
	return 0;
}

// dump params
void TunableParams::dump()
{
	for ( size_t i=0; i<params.size(); i++ )
	{
		std::cout << params[i]->name() << " = " << params[i]->get() << std::endl;
	}
}

size_t TunableParams::paramCount()
{
	return params.size();
}

const TunableBase *TunableParams::getParam( size_t index )
{
	return params[index];
}

TunableBase *TunableParams::findParam( const char *name )
{
	for (size_t i=0; i<params.size(); i++)
	{
		if (params[i]->name() == name) {
			return params[i];
		}
	}
	return 0;
}

}

#endif
