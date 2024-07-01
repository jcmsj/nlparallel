import time

from main import scan_both, scan_both_non_concurrent

# Prepare sample inputs
text = """
I'm at a payphone, trying to call home
All of my change I spent on you
Where have the times gone? Baby, it's all wrong
Where are the plans we made for two?
Yeah, I, I know it's hard to remember
The people we used to be
It's even harder to picture
That you're not here next to me
You say it's too late to make it
But is it too late to try?
And in our time that you wasted
All of our bridges burned down
I've wasted my nights
You turned out the lights
Now, I'm paralyzed
Still stuck in that time
When we called it love
But even the sun sets in paradise
I'm at a payphone, trying to call home
All of my change I spent on you
Where have the times gone? Baby, it's all wrong
Where are the plans we made for two?
If "Happy Ever After" did exist
I would still be holding you like this
All those fairy tales are full of shit
One more fucking love song, I'll be sick (oh)
You turned your back on tomorrow
'Cause you forgot yesterday
I gave you my love to borrow
But you just gave it away
You can't expect me to be fine
I don't expect you to care
I know I've said it before
But all of our bridges burned down
I've wasted my nights
You turned out the lights
Now, I'm paralyzed
Still stuck in that time
When we called it love
But even the sun sets in paradise
I'm at a payphone, trying to call home
All of my change I spent on you (oh, oh)
Where have the times gone? Baby, it's all wrong
Where are the plans we made for two? (Yeah)
If "Happy Ever After" did exist
I would still be holding you like this
And all those fairy tales are full of shit
One more fucking love song, I'll be sick (uh)
Now, I'm at a payphone
Man, fuck that shit
I'll be out spending all this money while you sitting 'round
Wondering why it wasn't you who came up from nothing
Made it from the bottom, now, when you see me, I'm stunning
And all of my cars start with a push of a button
Telling me had chances I blew up or whatever you call it
Switch the number to my phone, so you never could call it
Don't need my name on my show, you can tell that I'm balling
Swish, what a shame could have got picked
Had a really good game, but you missed your last shot
So you talk about who you see at the top
Or what you could've saw, but sad to say, it's over for
Phantom pulled up, valet open doors
Wished I'd go away, got what you was looking for
Now, it's me who they want, so you can go
And take that little piece of shit with you
I'm at a payphone, trying to call home
All of my change I spent on you (woo)
Where have the times gone? Baby, it's all wrong
Where are the plans we made for two? (Yeah, yeah)
If "Happy Ever After" did exist (oh, yeah)
I would still be holding you like this
All these fairy tales are full of shit
Yeah, one more fvcking love song, I'll be sick (yeah)
Now, I'm at a payphone
"""

distanceFil = 4
distanceEN = 4

import time
import argparse
if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description='Benchmark script')
    parser.add_argument('runs', type=int, default=10, help='Number of runs for each version. Defaults to 10')

    # Parse command line arguments
    args = parser.parse_args()

    # Assign run count from command line argument
    RUN_COUNT = args.runs

    # Accumulators for total execution times
    total_time_concurrent = 0
    total_time_non_concurrent = 0

    for _ in range(RUN_COUNT):
        # Benchmark concurrent version
        start_time_concurrent = time.time()
        result_concurrent = scan_both(text, distanceFil, distanceEN)
        end_time_concurrent = time.time()
        total_time_concurrent += (end_time_concurrent - start_time_concurrent)

        # Benchmark non-concurrent version
        start_time_non_concurrent = time.time()
        result_non_concurrent = scan_both_non_concurrent(text, distanceFil, distanceEN)
        end_time_non_concurrent = time.time()
        total_time_non_concurrent += (end_time_non_concurrent - start_time_non_concurrent)

    # Calculate average execution times
    avg_time_concurrent = total_time_concurrent / RUN_COUNT
    avg_time_non_concurrent = total_time_non_concurrent / RUN_COUNT

    # Print average execution times
    print(f"Average concurrent execution time: {avg_time_concurrent} seconds")
    print(f"Average non-concurrent execution time: {avg_time_non_concurrent} seconds")

    # Show which is faster in %
    if avg_time_concurrent < avg_time_non_concurrent:
        print(f"Concurrent version is {((avg_time_non_concurrent - avg_time_concurrent) / avg_time_non_concurrent) * 100}% faster")
    else:
        print(f"Non-concurrent version is {((avg_time_concurrent - avg_time_non_concurrent) / avg_time_concurrent) * 100}% faster")
