[y,Fs] = audioread('01_how-can-i-succeed-in-this-course.mp4');
v = VideoReader('01_how-can-i-succeed-in-this-course.mp4');
%sound(y,Fs);
T = 1/Fs;
L = v.Duration*1000;
x = fft(y);

P2 = abs(y/L);
P1 = P2(1:floor(L/2)+1);
P1(2:end-1) = 2*P1(2:end-1);
mn = mean2(P1);
for i = 1:length(P1)
    if(P1(i)<=mn)
        P1(i)=NaN;
    end
end

f = Fs*(0:(L/2))/L;
subplot(2,1,1);
plot(f,P1) 
title('Filetered Magnitudes')
xlabel('f (Hz)')
ylabel('|P1(f)|')

subplot(2,1,2);
der = diff(P1);
f1 = f(2:end)';
plot(f1,der) 
title('Derivative')
xlabel('f (Hz)')
ylabel('|P1(f)|')


