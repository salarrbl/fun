#!/usr/bin/env bash

# # Cleanup function to handle script exit
# cleanup() {
#     echo "Exiting... Goodbye! :)"
#     killall mpg123 2>/dev/null
#     exit 0
# }

# # Trap Ctrl+C to run cleanup
# trap cleanup SIGINT

# # Start mpg123 with random mode in the background and suppress logs
# mpg123 -q -z ~/Music/youtube/* &

# # Run cava in the background (visualizer)
# cava 

# while true; do
#     # echo "Press 'f' to skip track, 'd' for other actions. Press Ctrl+C to stop."

#     # Read a single character input
#     read -n 1 -s key

#     case $key in
#         f)
#             echo "You pressed 'f'. Skipping to the next track!"
#             killall mpg123 2>/dev/null # Kill the current mpg123 process
#             mpg123 --next ~/Music/youtube/* & # Restart mpg123 with a random track
#             ;;
#         d)
#             echo "You pressed 'd'. Performing another action!"
#             # Add another custom action here
#             ;;
#         *)
#             echo "Unrecognized key: $key"
#             ;;
#     esac

#     sleep 0.5
# done

# Cleanup function to handle script exit
cleanup() {
    echo "Exiting... Goodbye! :)"
    killall mpg123 2>/dev/null
    killall cava 2>/dev/null
    exit 0
}

# Trap Ctrl+C to run cleanup
trap cleanup SIGINT

# Start mpg123 with random mode in the background and suppress logs
mpg123 -q -z ~/Music/everything/* &

# Run cava in the background
cava 

while true; do
    # Read a single character input silently
    read -n 1 -s key

    case $key in
        f)
            echo "You pressed 'f'. Skipping to the next track!"
            killall mpg123 2>/dev/null # Kill the current mpg123 process
            mpg123 -q -z ~/Music/youtube/* & # Restart mpg123 with a random track
            ;;
        d)
            echo "You pressed 'd'. Performing another action!"
            # Add another custom action here
            ;;
        *)
            echo "Unrecognized key: $key"
            ;;
    esac

    sleep 0.01
done

