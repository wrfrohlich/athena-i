//------------------------------------------------------------------------------
//
//			Name: Eng. William da Rosa Frohlich
//
//			Project: Acquisition of BITalino Data
//
//			Date: 2020.06.13
//
//			Update: 2021.04.19
//
//------------------------------------------------------------------------------
// Libraries

#include "bitalino.h"
#include <iostream>
#include <fstream>
#include <time.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>

using namespace std;

//------------------------------------------------------------------------------

#ifdef _WIN32

#include <conio.h>

bool keypressed(void)
{
	return (_kbhit() != 0);
}

//------------------------------------------------------------------------------

#else // Linux or Mac OS

#include <sys/select.h>

bool keypressed(void)
{
   fd_set   readfds;
   FD_ZERO(&readfds);
   FD_SET(0, &readfds);

   timeval  readtimeout;
   readtimeout.tv_sec = 0;
   readtimeout.tv_usec = 0;

   return (select(FD_SETSIZE, &readfds, NULL, NULL, &readtimeout) == 1);
}

#endif

//------------------------------------------------------------------------------

int main(int argc, char **argv)
{
//------------------------------------------------------------------------------
// Variable
	int sockfd;
	sockfd = socket(AF_INET,SOCK_DGRAM,0);
	struct sockaddr_in serv;
	char msg[44], ECG[5], EDA[5], RSP[5], current_time[20], name[20], new_name[21], control[5];
	
	// Socket
	serv.sin_family = AF_INET;
	serv.sin_port = htons(18000);
	serv.sin_addr.s_addr = inet_addr("127.0.0.1");
	socklen_t m = sizeof(serv);
	
	string file_name;
	string start_name = "/var/log/athena-i/raw/";
	string end_name = ".txt";
	string s_day, s_month, s_year, s_hour, s_reference_time, s_min, s_sec;
	
	time_t date_time;
	
	time(&date_time);
	
	struct tm*get_date = localtime(&date_time);
	struct tm*get_time = localtime(&date_time);
	
	int i_day = get_date->tm_mday;
	int i_month = get_date->tm_mon + 1;
	int i_year = get_date->tm_year + 1900;
	int i_hour = get_time->tm_hour;
	int i_min = get_time->tm_min;
	int i_sec = get_time->tm_sec;

	int reference_time = get_time->tm_min;
	
	s_day = std::to_string(i_day);
	s_month = std::to_string(i_month);
	s_year = std::to_string(i_year);
	s_hour = std::to_string(i_hour);
	s_min = std::to_string(i_min);

	file_name = start_name + argv[1] + "_" + argv[2] + "_" + s_day  + "-" + s_month + "-" + s_year + "_" + s_hour + "_" + s_min + end_name;
	
//------------------------------------------------------------------------------

	try
	{
		// Starts the file
		ofstream myfile;
		
		//snprintf(name, 20, "%s %s", argv[1], argv[2]);
		
		// Waiting for Connection
		puts("Connecting to device. Please, wait a moment.");
		
		// Set the MAC address
		BITalino dev("98:D3:21:FC:8B:64");  // Device MAC address (Windows and Linux)
		
		// Message about the defice connected
		puts("Device Connected. Press Enter to exit.");
		
		// Create the file
		myfile.open (file_name, ios::app);
		
		// Define the categories of the file
		myfile << "NAME;SURNAME;ECG;EDA;RSP;TIME\n";
		
		// Close the file
		myfile.close();
		
		// Get device version and show
		std::string ver = dev.version();
		printf("BITalino version: %s\n", ver.c_str());
		
		// Start acquisition of all channels at 1000 Hz
		dev.start(1000, { 0, 1, 2, 3, 4, 5});
		dev.trigger({true, false});
		
//------------------------------------------------------------------------------
// Start Loop

		// Initialize the frames vector with 1 frames
		BITalino::VFrame frames(1);
		do
		{
			// Get frames
			dev.read(frames);
			const BITalino::Frame &f = frames[0];
						
			// Get the current time
			date_time;
			time(&date_time);
			
			tm*get_date = localtime(&date_time);
			tm*get_time = localtime(&date_time);
			
			i_day = get_date->tm_mday;
			i_month = get_date->tm_mon + 1;
			i_year = get_date->tm_year + 1900;
			i_min = get_time->tm_min;
			i_hour = get_time->tm_hour;
			i_sec = get_time->tm_sec;
			
			if ((reference_time + 1) == i_min)
			{
				if(connect(sockfd, (struct sockaddr *)&serv, sizeof(struct sockaddr)) < 0)
				{
					close(sockfd);
					cout << "socket: closed\n";
					sockfd = socket(AF_INET,SOCK_DGRAM,0);
					serv.sin_family = AF_INET;
					serv.sin_port = htons(18000);
					serv.sin_addr.s_addr = inet_addr("127.0.0.1");
					socklen_t m = sizeof(serv);

					if(connect(sockfd, (struct sockaddr *)&serv, sizeof(struct sockaddr)) < 0)
					{
						cout << "socket: error open\n";
						close(sockfd);
						return 0;
					}
				}

				if (reference_time == -1)
				{
					sprintf(msg, "%s;%d-%d-%d_%d_%d", "READ", i_day, i_month, i_year, i_hour, 59);
				}
				else
				{
					sprintf(msg, "%s;%d-%d-%d_%d_%d", "READ", i_day, i_month, i_year, i_hour, reference_time);
				}

				
				sendto(sockfd, msg, strlen(msg), 0, (struct sockaddr *)&serv, m);
				cout << "message: sent\n";

				s_day = std::to_string(i_day);
				s_month = std::to_string(i_month);
				s_year = std::to_string(i_year);
				s_hour = std::to_string(i_hour);
				s_min = std::to_string(i_min);
				
				file_name = start_name + argv[1] + "_" + argv[2] + "_" + s_day  + "-" + s_month + "-" + s_year + "_" + s_hour + "_" + s_min + end_name;
				
				// Create the file
				myfile.open (file_name, ios::app);
				
				// Define the categories of the file
				myfile << "NAME;SURNAME;ECG;EDA;RSP;TIME\n";
				
				// Close the file
				myfile.close();

				if (i_min == 59)
				{
					reference_time = -1;
				}
				else
				{
					reference_time++;
				}
			}

			// Open the file
			myfile.open (file_name, ios::app);

			sprintf(msg, "%s;%s;%d;%d;%d;%d/%d/%d %d:%d:%d", argv[1], argv[2], f.analog[0], f.analog[1], f.analog[2], i_day, i_month, i_year, i_hour, i_min, i_sec);

			// Save the data in the file
			myfile << msg << "\n";
			
			// Close the file
			myfile.close();
		
		// Until the key is pressed
		} while (true);
//------------------------------------------------------------------------------
// End Loop

	}
	catch(BITalino::Exception &e)
	{
		if(connect(sockfd, (struct sockaddr *)&serv, sizeof(struct sockaddr)) < 0)
		{
			close(sockfd);
			cout << "socket: closed\n";
			sockfd = socket(AF_INET,SOCK_DGRAM,0);
			serv.sin_family = AF_INET;
			serv.sin_port = htons(18000);
			serv.sin_addr.s_addr = inet_addr("127.0.0.1");
			socklen_t m = sizeof(serv);

			if(connect(sockfd, (struct sockaddr *)&serv, sizeof(struct sockaddr)) < 0)
			{
				cout << "socket: error open\n";
				close(sockfd);
				return 0;
			}
		}
		
		sprintf(msg, "%s;%d-%d-%d_%d_%d", "STOP", i_day, i_month, i_year, i_hour, reference_time);
		sendto(sockfd, msg, strlen(msg), 0, (struct sockaddr *)&serv, m);
		printf("BITalino exception: %s\n", e.getDescription());
		close(sockfd);
	}
	return 0;
}
//------------------------------------------------------------------------------