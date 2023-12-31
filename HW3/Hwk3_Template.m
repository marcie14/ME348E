% Written by Ann Majewicz Fey
% Template Code for HWK3

clear all
close all

t = 0:0.1:10;
dt = 0.1;
theta = zeros(1,length(t));
x = zeros(1,length(t));
y = zeros(1,length(t));

l = 4.92; % Wheel Base (wheel to wheel distance)
d =  2.7559055; % Diameter of wheel
c = pi*d; %  Circumference of wheel -  total travel in 1 rotation


% ===== Simple Rotation Motion =====
omega_left = -90*pi/180; %rad/sec;
omega_right = 90*pi/180; %deg/sec;
vl = omega_left*d/2;
vr = omega_right*d/2;

for i = 2:length(t) 
    % FILL OUT THE EQUATIONS HERE FOR PURE ROTATION
    % Left Riemann sum = integral
    x(i) = x(i-1); % HINT
    
    y(i) = y(i-1);
    theta(i) = theta(i-1) + 2*vr*dt/l;
end

figure 
plot(t,x)
hold on 
plot(t,y)
xline(7.14097)
yyaxis left
plot(t,theta.*180/pi)
legend('x','y','theta')
xlabel('time (s)')


% ===== Simple Linear Motion =====
omega_both = 90*pi/180; %rad/sec;
v = omega_both*d/2;

for i = 2:length(t)
% FILL OUT THE EQUATIONS HERE FOR PURE TRANSLATION
    x(i) = x(i-1) + v*cos(theta(i-1))*dt; % HINT
    y(i) = y(i-1) + v*sin(theta(i-1))*dt;
    theta(i) = theta(i-1);
end

figure 
plot(t,x)
hold on 
plot(t,y)
yyaxis left
plot(t,theta.*180/pi)
legend('x','y','theta')
xlabel('time (s)')

figure 
plot(x,y)
xlabel('x (in)')
ylabel('y (in)')

% ===== Compound Motion =====
% In this step, show a simulation of the robot moving to 
% be positioned in front of the top right basket
% (similar to the line following demo). The robot needs to move 
% forward for 18+24 inches, turn 90 deg to the right and forward 
% for 21 inches, followed by another 90 turn to the left to face
% the basket. In this step, 
tcompound = 0:0.1:50;
dt = 0.1;
thetaComp = zeros(1,length(tcompound));
xComp = zeros(1,length(tcompound));
yComp = zeros(1,length(tcompound));

% Create a vector for forward velocity 
%======================================
omega_left = zeros(1,length(tcompound));
omega_right = zeros(1,length(tcompound));

% WRITE SOME CODE TO FILL OUT WHAT THE NEW 
% OMEGA VECTORS SHOULD BE FOR THE COMPOUND 
% MOVEMENT. 
% Consider adding vectors you want peicewise, 
% repmat is a useful function to copy values

%omega_left = xx; %rad/sec;
%omega_right = xx; %deg/sec;

for i = 2:length(tcompound) 
  % NOW WRITE THE FUNCTIONS TO MAP OMEGA INTO NEW X, Y, and Theta
  %==============
    % NOTE: yours will be a little more complicated since 
    % you have a different set of equations for a turn vs. going straight.
    % You may want consider an if statement to check if both wheels 
    % are spinning at the same speed or not. 
    %xComp(i) = xx; 
    %yComp(i) = xx
    %thetaComp(i) = xx;
    if (yComp(i)<42)
        xComp(i) = xComp(i-1) + v*sin(theta(i-1))*dt;
        yComp(i) = yComp(i-1) + v*cos(theta(i-1))*dt;
        theta(i)=theta(i-1);
    elseif (yComp(i)==42 && theta(i) < 3.14)
        xComp(i) = xComp(i-1);
        yComp(i) = yComp(i-1);
        theta(i) = theta(i-1) + 2*vr*dt/l;
    elseif xComp(i)<21 && theta(i)==pi
        xComp(i) = xComp(i-1) + v*sin(theta(i-1))*dt;
        yComp(i) = yComp(i-1) + v*cos(theta(i-1))*dt;
        theta(i)=theta(i-1);
    elseif (xComp(i)==21 && theta(i)>0)
        xComp(i) = xComp(i-1);
        yComp(i) = yComp(i-1);
        theta(i) = theta(i-1) + 2*vl*dt/l;
    else
        xComp(i) = xComp(i-1);
        yComp(i) = yComp(i-1);
        theta(i) = theta(i-1);
    end
    
end

% NOW PLOT YOUR RESULTS TO SHOW YOU CAN REACH THE TARGET
 figure 
 plot(tcompound,xComp)
 hold on 
 plot(tcompound,yComp)
 yyaxis left
 plot(tcompound,theta.*180/pi)
 legend('x','y','theta')
 xlabel('time (s)')
 
 figure 
 plot(xComp,yComp)
 xlabel('x (in)')
 ylabel('y (in)')


